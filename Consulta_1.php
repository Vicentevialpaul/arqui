<!DOCTYPE html>
<html>
<style>
table, th, td {
    border: 1px solid black;
}
</style>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
</head>
<body>

<?php
  include_once "psql-config.php";
  try {
    $db = new PDO("pgsql:dbname=".DATABASE.";host=".HOST.";port=".PORT.";user=".USER.";password=".PASSWORD);
    }
    catch(PDOException $e) {
    echo $e->getMessage();
    }
    $numero_cuenta = $_POST["numero_cuenta"];
    $fecha = $_POST["fecha"];

 $query = "SELECT  transfiere.cuenta_banco_comprador, transfiere.cuenta_banco_vendedor, transferencia.cant_zorzales FROM transfiere,transferencia where 

(transfiere.cuenta_banco_comprador =  $numero_cuenta or transfiere.cuenta_banco_vendedor =  $numero_cuenta) and  transferencia.fecha = '$fecha'  and transfiere.id_trans = transferencia.id_trans ;"

 ;


	$result = $db -> prepare($query);
	$result -> execute();
	# Ojo, fetch() nos retorna la primer fila, fetchAll()
	# retorna todas.
	$consulta_general = $result -> fetchAll();
	echo "<table><tr><th>Comprador</th><th>Vendedor</th><th>Cantidad</th></tr>";
	foreach ($consulta_general as $consulta) {
  		echo "<tr><td>$consulta[0]</td><td>$consulta[1]</td><td>$consulta[2]</td><</tr>";
	}
	echo "</table>";


?>

<form action="index.php" method="post">
  <input type="submit" value="Volver">
</form> 
</body>
</html>