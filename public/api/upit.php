<?php
declare(strict_types=1);

// Configuration stays outside every webroot. No credentials belong in this file.
const UPIT_ERROR = 'Nešto nije prošlo. Pozovite nas ili pišite na office@easy.rs.';

function validate_upit(array $input, int $now): array
{
    $limits = ['ime' => 100, 'firma' => 150, 'telefon' => 40, 'email' => 254,
        'racunari' => 20, 'poruka' => 2000, 'proizvod' => 300, 'website' => 200, 'ts' => 12];
    $data = [];
    foreach ($limits as $key => $limit) {
        $value = $input[$key] ?? '';
        if (!is_string($value) && !is_int($value)) {
            throw new InvalidArgumentException('Proverite unete podatke.');
        }
        $value = trim((string) $value);
        if (!preg_match('//u', $value) || preg_match_all('/./us', $value) > $limit || str_contains($value, "\0")) {
            throw new InvalidArgumentException('Proverite dužinu i sadržaj unetih podataka.');
        }
        if ($key !== 'poruka' && preg_match('/[\r\n]/', $value)) {
            throw new InvalidArgumentException('Proverite unete podatke.');
        }
        $data[$key] = $value;
    }
    if ($data['website'] !== '' || !ctype_digit($data['ts']) || $now - (int) $data['ts'] <= 3) {
        throw new InvalidArgumentException('Sačekajte nekoliko sekundi pa pokušajte ponovo.');
    }
    foreach (['ime', 'telefon', 'poruka'] as $key) {
        if ($data[$key] === '') {
            throw new InvalidArgumentException('Popunite ime i prezime, telefon i poruku.');
        }
    }
    if (!preg_match('/^[+0-9() .\/-]{6,40}$/', $data['telefon']) || strlen(preg_replace('/\D/', '', $data['telefon'])) < 6) {
        throw new InvalidArgumentException('Unesite ispravan broj telefona.');
    }
    if ($data['email'] !== '' && !filter_var($data['email'], FILTER_VALIDATE_EMAIL)) {
        throw new InvalidArgumentException('Unesite ispravnu email adresu.');
    }
    if (!in_array($data['racunari'], ['', '1–5', '6–10', '11–20', '20+', 'nije bitno'], true)) {
        throw new InvalidArgumentException('Izaberite broj računara iz ponuđene liste.');
    }
    return $data;
}

function upit_body(array $data): string
{
    $labels = ['ime' => 'Ime i prezime', 'firma' => 'Firma', 'telefon' => 'Telefon',
        'email' => 'Email', 'racunari' => 'Broj računara', 'proizvod' => 'Proizvod', 'poruka' => 'Poruka'];
    $lines = ['🟢 UPIT sa easy.rs'];
    foreach ($labels as $key => $label) {
        $lines[] = $label . ': ' . ($data[$key] ?: '—');
    }
    return implode("\n", $lines);
}

function deliver_upit(array $data, callable $telegram, callable $email): bool
{
    $body = upit_body($data);
    $success = false;
    foreach (['telegram' => $telegram, 'email' => $email] as $name => $send) {
        try {
            $ok = $send($data, $body) === true;
        } catch (Throwable $error) {
            $ok = false;
        }
        if (!$ok) error_log('easy.rs upit: ' . $name . ' delivery failed');
        $success = $ok || $success;
    }
    return $success;
}

function telegram_upit(array $data, string $body): bool
{
    if (!defined('TG_TOKEN') || !defined('TG_CHAT') || !TG_TOKEN || !TG_CHAT || !function_exists('curl_init')) return false;
    $request = curl_init('https://api.telegram.org/bot' . TG_TOKEN . '/sendMessage');
    curl_setopt_array($request, [CURLOPT_POST => true, CURLOPT_RETURNTRANSFER => true,
        CURLOPT_CONNECTTIMEOUT => 3, CURLOPT_TIMEOUT => 8,
        CURLOPT_HTTPHEADER => ['Content-Type: application/json'],
        CURLOPT_POSTFIELDS => json_encode(['chat_id' => TG_CHAT, 'text' => $body], JSON_UNESCAPED_UNICODE | JSON_THROW_ON_ERROR)]);
    $response = curl_exec($request);
    $status = curl_getinfo($request, CURLINFO_HTTP_CODE);
    curl_close($request);
    return $status === 200 && is_string($response) && (json_decode($response, true)['ok'] ?? false) === true;
}

function email_upit(array $data, string $body): bool
{
    if (!defined('MAIL_TO') || !defined('MAIL_FROM') || !filter_var(MAIL_TO, FILTER_VALIDATE_EMAIL)
        || !filter_var(MAIL_FROM, FILTER_VALIDATE_EMAIL)) return false;
    $subject = 'Upit sa easy.rs — ' . $data['ime'] . ($data['firma'] !== '' ? ' (' . $data['firma'] . ')' : '');
    // Fold RFC 2047 encoded words without splitting a UTF-8 code point.
    preg_match_all('/.{1,12}/us', $subject, $chunks);
    $subject = implode("\r\n ", array_map(fn($part) => '=?UTF-8?B?' . base64_encode($part) . '?=', $chunks[0]));
    $headers = ['From' => MAIL_FROM, 'MIME-Version' => '1.0',
        'Content-Type' => 'text/plain; charset=UTF-8', 'Content-Transfer-Encoding' => '8bit'];
    if ($data['email'] !== '') $headers['Reply-To'] = $data['email'];
    return mail(MAIL_TO, $subject, $body, $headers);
}

function allow_upit(string $ip, string $directory, int $now): bool
{
    if (!is_dir($directory) && !mkdir($directory, 0700, true) && !is_dir($directory)) return false;
    $file = fopen($directory . '/' . hash('sha256', $ip) . '.json', 'c+');
    if (!$file) return false;
    if (!flock($file, LOCK_EX)) { fclose($file); return false; }
    $attempts = json_decode(stream_get_contents($file), true);
    $attempts = is_array($attempts) ? array_values(array_filter($attempts, fn($time) => is_int($time) && $time > $now - 600)) : [];
    $allowed = count($attempts) < 5;
    if ($allowed) $attempts[] = $now;
    rewind($file);
    ftruncate($file, 0);
    fwrite($file, json_encode($attempts));
    fflush($file);
    flock($file, LOCK_UN);
    fclose($file);
    return $allowed;
}

function respond_upit(int $status, string $message, array $input = []): never
{
    header('Cache-Control: no-store');
    header('X-Content-Type-Options: nosniff');
    $json = str_contains($_SERVER['HTTP_ACCEPT'] ?? '', 'application/json')
        || str_contains($_SERVER['CONTENT_TYPE'] ?? '', 'application/json');
    if ($status === 200 && !$json) {
        header('Location: /hvala', true, 303);
        exit;
    }
    http_response_code($status);
    if ($json) {
        header('Content-Type: application/json; charset=UTF-8');
        echo json_encode(['ok' => $status === 200, 'error' => $status === 200 ? null : $message], JSON_UNESCAPED_UNICODE);
    } else {
        header('Content-Type: text/html; charset=UTF-8');
        $escape = fn($value) => htmlspecialchars(is_scalar($value) ? (string) $value : '', ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
        echo '<!doctype html><html lang="sr-Latn"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Upit — Easy Computers</title>';
        echo '<main style="max-width:42rem;margin:3rem auto;padding:1rem;font:18px/1.6 system-ui;color:#0f2c4e"><h1>Upit nije poslat</h1><p>' . $escape($message) . '</p>';
        echo '<p>Vaši podaci su sačuvani ispod. Možete da ih kopirate ili ponovite slanje.</p><form method="post" action="/api/upit.php">';
        foreach (['ime' => 'Ime i prezime', 'firma' => 'Firma', 'telefon' => 'Telefon', 'email' => 'Email', 'racunari' => 'Broj računara', 'proizvod' => 'Proizvod', 'poruka' => 'Poruka'] as $key => $label) {
            echo '<label style="display:block;margin-top:1rem">' . $label . '<textarea style="display:block;width:100%;font:inherit" name="' . $key . '">' . $escape($input[$key] ?? '') . '</textarea></label>';
        }
        echo '<input type="hidden" name="ts" value="' . time() . '"><button style="margin-top:1rem;padding:.75rem" type="submit">Pokušajte ponovo</button></form><p><a href="tel:+381631111727">Pozovite nas</a> · <a href="mailto:office@easy.rs">office@easy.rs</a></p></main></html>';
    }
    exit;
}

function handle_upit(): never
{
    if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
        header('Allow: POST');
        respond_upit(405, 'Koristite kontakt formu za slanje upita.');
    }
    if ((int) ($_SERVER['CONTENT_LENGTH'] ?? 0) > 16384) respond_upit(413, 'Poruka je predugačka.');
    $input = $_POST;
    if (str_contains($_SERVER['CONTENT_TYPE'] ?? '', 'application/json')) {
        $raw = file_get_contents('php://input', false, null, 0, 16385);
        if ($raw === false || strlen($raw) > 16384) respond_upit(413, 'Poruka je predugačka.');
        $input = json_decode($raw, true);
        if (!is_array($input)) respond_upit(400, 'Neispravan format upita.');
    }
    try {
        $data = validate_upit($input, time());
    } catch (InvalidArgumentException $error) {
        respond_upit(422, $error->getMessage(), $input);
    }
    try {
        if (!is_file('/www/easy-config/config.php')) throw new RuntimeException('Missing config');
        require '/www/easy-config/config.php';
        if (!allow_upit($_SERVER['REMOTE_ADDR'] ?? 'unknown', '/www/easy-config/rate-limit', time())) {
            header('Retry-After: 600');
            respond_upit(429, 'Poslali ste više upita. Pokušajte za deset minuta ili nas pozovite.', $input);
        }
        $ok = deliver_upit($data, 'telegram_upit', 'email_upit');
    } catch (Throwable $error) {
        error_log('easy.rs upit: configuration or transport error');
        $ok = false;
    }
    respond_upit($ok ? 200 : 503, UPIT_ERROR, $input);
}

// Tests can include the functions without invoking external delivery.
if (realpath($_SERVER['SCRIPT_FILENAME'] ?? '') === __FILE__) handle_upit();
