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
    

 	$query = "SELECT t.id_trans,tra.cuenta_banco_comprador,tra.cuenta_banco_vendedor,t.cant_zorzales, t.fecha 
  from Transferencia as t, transfiere as tra
   where t.fecha in (select max(t1.fecha) from Transferencia as t1, transfiere as tr where tr.id_trans = t1.id_trans and 
    (tr.cuenta_banco_comprador =  $numero_cuenta or tr.cuenta_banco_vendedor =  $numero_cuenta)) and
    t.id_trans = tra.id_trans and 
    (tra.cuenta_banco_comprador =  $numero_cuenta or tra.cuenta_banco_vendedor =  $numero_cuenta) ;";

	$result = $db -> prepare($query);
	$result -> execute();
	# Ojo, fetch() nos retorna la primer fila, fetchAll()
	# retorna todas.
  $consulta_general = $result -> fetchAll();
  echo "<table><tr><th>id trans</th><th>comprador</th><th>vendedor</th><th>cantidad</th><th>fecha</th></tr>";
  foreach ($consulta_general as $consulta) {
      echo "<tr><td>$consulta[0]</td><td>$consulta[1]</td><td>$consulta[2]</td><td>$consulta[3]</td><td>$consulta[4]</td></tr>";
  }
	echo "</table>";


?>

<form action="index.php" method="post">
  <input type="submit" value="Volver">
</form> 
</body>
</html>