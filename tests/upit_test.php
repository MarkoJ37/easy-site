<?php
require __DIR__ . '/../public/api/upit.php';
function check(bool $ok, string $name): void {
    if (!$ok) throw new RuntimeException($name);
    echo "PASS: $name\n";
}
$input = ['ime' => 'Željko Đurić', 'telefon' => '+381 61 1234567', 'poruka' => "Test\nDrugi red", 'ts' => '100', 'racunari' => '1–5'];
$data = validate_upit($input, 105);
check($data['ime'] === $input['ime'], 'UTF-8 valid input');
foreach ([['website' => 'spam'], ['ts' => '104'], ['ts' => '200'], ['ime' => ''], ['email' => "a@b.com\r\nBcc: x@y.com"], ['ime' => ['array']], ['poruka' => str_repeat('a', 2001)], ['telefon' => 'abc123'], ['racunari' => '999']] as $bad) {
    try { validate_upit(array_replace($input, $bad), 105); throw new RuntimeException('Invalid input accepted'); }
    catch (InvalidArgumentException $expected) { echo 'PASS: rejects ' . array_key_first($bad) . "\n"; }
}
foreach ([[true, true], [false, true], [true, false], [false, false]] as [$tg, $mail]) {
    $calls = 0;
    $result = deliver_upit($data, function() use ($tg, &$calls) { $calls++; return $tg; }, function() use ($mail, &$calls) { $calls++; return $mail; });
    check($result === ($tg || $mail) && $calls === 2, 'Both channels attempted; one success sufficient');
}
check(deliver_upit($data, fn() => throw new RuntimeException('transport'), fn() => true), 'Exception in Telegram still tries email');
$directory = sys_get_temp_dir() . '/easy-upit-test-' . bin2hex(random_bytes(8));
for ($i = 0; $i < 5; $i++) check(allow_upit('127.0.0.1', $directory, 100), 'Allowed within limit');
check(!allow_upit('127.0.0.1', $directory, 101), 'Rate limit blocks sixth attempt');
check(allow_upit('127.0.0.1', $directory, 701), 'Rate limit expires');
unlink($directory . '/' . hash('sha256', '127.0.0.1') . '.json');
rmdir($directory);
