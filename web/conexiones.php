<?php

// Conexion general con la base de datos

$host = 'sql308.infinityfree.com'; 
$db = 'if0_38659913_libreria'; 
$user = 'if0_38659913'; 
$pass = 'Alejandro240604'; 

try {
    $pdo = new PDO("mysql:host=$host;dbname=$db;charset=utf8", $user, $pass);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch (PDOException $e) {
    echo "Error de conexión: " . $e->getMessage();
}
?>
