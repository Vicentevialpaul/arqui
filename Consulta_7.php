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

    

 	$query1 = "SELECT sum(e.cantidad_zorzales) from Exchange as e where e.id_exchange = $numero_cuenta ;";
  $result = $db -> prepare($query1);
  $result -> execute();
  # Ojo, fetch() nos retorna la primer fila, fetchAll()
  # retorna todas.
  $query1 = $result -> fetch();
  $query1 = $query1[0];
  $query2 = "SELECT sum(t.cant_zorzales) from Transferencia as t, transfiere as tr where t.id_trans = tr.id_trans 
  and tr.cuenta_banco_comprador = $numero_cuenta;";
  $result = $db -> prepare($query2);
  $result -> execute();
  # Ojo, fetch() nos retorna la primer fila, fetchAll()
  # retorna todas.
  $query2 = $result -> fetch();
  $query2 = $query2[0];
  $query3 = "SELECT sum(t.cant_zorzales) from Transferencia as t, transfiere as tr where t.id_trans = tr.id_trans 
  and tr.cuenta_banco_vendedor = $numero_cuenta;"; 
  $result = $db -> prepare($query3);
  $result -> execute();
  # Ojo, fetch() nos retorna la primer fila, fetchAll()
  # retorna todas.
  $query3 = $result -> fetch();
  $query3 = $query3[0];
  $query = intval($query1) + intval($query2) - intval($query3) ;

	echo "</table>";
  echo "<table><tr><th>cantidad_zorzales</th></tr>";
  echo "<table><tr><th>$query</th></tr>";
  echo "</table>";



?>

<form action="index.php" method="post">
  <input type="submit" value="Volver">
</form> 
</body>
</html>