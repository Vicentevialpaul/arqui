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
    $cantidad= $_POST["cantidad"];
    $cantidad = intval($cantidad);
    $dia = $_POST["dia"];

 	$query = "SELECT cant_peso_x_zorzal* $cantidad, cant_dolar_x_zorzal * $cantidad  FROM PrecioHistorico  WHERE fecha = '$dia' ;";




	$result = $db -> prepare($query);
	$result -> execute();
	# Ojo, fetch() nos retorna la primer fila, fetchAll()
	# retorna todas.
  $consulta_general = $result -> fetchAll();
  echo "<table><tr><th>pesos</th><th>dolar</th><th>...</th></tr>";
  foreach ($consulta_general as $consulta) {
      echo "<tr><td>$consulta[0]</td><td>$consulta[1]</td></tr>";
  }
	echo "</table>";


?>

<form action="index.php" method="post">
  <input type="submit" value="Volver">
</form> 
</body>
</html>