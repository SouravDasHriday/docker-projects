<?php
// These are the details for the connection.
// The host is 'db' because that is the name of our database service in docker-compose.yml.
$host = 'db';
$user = 'myuser';
$pass = 'mypassword';
$db_name = 'mydatabase';

// Create a new mysqli connection
$conn = new mysqli($host, $user, $pass, $db_name);

// Check for connection errors
if ($conn->connect_error) {
    die("<h1>Connection failed: " . $conn->connect_error . "</h1>");
}

echo "<h1>🔥 Successfully connected to MySQL! 🔥</h1>";
echo "<h2>My Awesome LAMP Stack is running via Docker Compose.</h2>";

// Query the database to get the data
$sql = 'SELECT * FROM products';
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    echo "<h3>Products from our Database:</h3>";
    echo "<ul>";
    // output data of each row
    while($row = $result->fetch_assoc()) {
        echo "<li>ID: " . $row["id"]. " - Name: " . $row["name"]. "</li>";
    }
    echo "</ul>";
} else {
    echo "0 results";
}

$conn->close();
?>
