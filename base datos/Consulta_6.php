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
    
    

   $query = "SELECT tr.fecha, count(*) FROM Transferencia as tr group by tr.fecha  Having 
   tr.fecha >= '05 Dec 2000' and tr.fecha <= '24 Dec 2000' and count(*) = (
   SELECT max(q.c) from (SELECT t.fecha , count(*) as c FROM Transferencia as t group by t.fecha  Having 
   t.fecha >= '05 Dec 2000' and t.fecha <= '24 Dec 2000') as q);" ;

   $query1 = "SELECT tr.fecha, sum(tr.cant_zorzales) FROM Transferencia as tr group by tr.fecha  Having 
   tr.fecha >= '05 Dec 2000' and tr.fecha <= '24 Dec 2000' and sum(tr.cant_zorzales) = (
   SELECT max(q.c) from (SELECT t.fecha , sum(t.cant_zorzales) as c FROM Transferencia as t group by t.fecha  Having 
   t.fecha >= '01 Dec 2000' and t.fecha <= '31 Dec 2000') as q);" ;






	$result = $db -> prepare($query);
	$result -> execute();
	# Ojo, fetch() nos retorna la primer fila, fetchAll()
	# retorna todas.
  $consulta_general = $result -> fetchAll();
  echo "<table><tr><th>dia mayor cantidad transferencias</th><th>cantidad</th><th>...</th></tr>";
  foreach ($consulta_general as $consulta) {
      echo "<tr><td>$consulta[0]</td><td>$consulta[1]</td></tr>";
  }
	echo "</table>";

  $result = $db -> prepare($query1);
  $result -> execute();
  # Ojo, fetch() nos retorna la primer fila, fetchAll()
  # retorna todas.
  $consulta_general = $result -> fetchAll();
  echo "<table><tr><th>dia mayor cantidad zorzales</th><th>cantidad</th><th>...</th></tr>";
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