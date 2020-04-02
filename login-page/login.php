<!doctype html>
<html lang="en">
  <head >
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
    <title>Login</title>
  </head>
  <body class="mx-auto" style="width: 200px;">

    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="https://code.jquery.com/jquery-3.4.1.slim.min.js" integrity="sha384-J6qa4849blE2+poT4WnyKhv5vZF5SrPo0iEjwBvKU7imGFAV0wwj1yYfoRSJoZ+n" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js" integrity="sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6" crossorigin="anonymous"></script>

<?php require ("./vendor/autoload.php");
require ('connection.php');
//Step 1: Enter you google account credentials
$g_client = new Google_Client();

$g_client->setClientId("1038416313130-0spncpo5g1tiqrl7u44e9ji8o4qvlt6q.apps.googleusercontent.com");
$g_client->setClientSecret("0PskUDFqYJDDSATiLavlShnI");
$g_client->setRedirectUri("http://localhost/ESD-G5T4/login-page/login.php");
$g_client->setScopes("email");
$g_client->addScope("profile");
$g_client->setAccessType('offline');
$g_client->setApprovalPrompt('force');

//Step 2 : Create the url
$auth_url = $g_client->createAuthUrl();
echo "<br>";

//Step 3 : Get the authorization  code
$code = isset($_GET['code']) ? $_GET['code'] : NULL;
//Step 4: Get access token
if(isset($code)) {
    try {
        $token = $g_client->fetchAccessTokenWithAuthCode($code);
        $g_client->setAccessToken($token);

    }catch (Exception $e){
        echo $e->getMessage();
    }
    try {
        $pay_load = $g_client->verifyIdToken();
        echo $pay_load['email'];
        echo $pay_load['name'];


    }catch (Exception $e) {
        echo $e->getMessage();
    }

} else{
    $pay_load = null;
}
if(isset($pay_load)){
    $name = $pay_load['name'];
    $email = $pay_load['email'];
    $email = mysqli_real_escape_string($mysqli, $email);
    $result = mysqli_query($mysqli, "SELECT * FROM login WHERE email='$email' ")
        or die("Could not execute the select query.");
    
    $row = mysqli_fetch_assoc($result);
    $id = $row['id'];
    
    if(is_array($row) && !empty($row)) {
        // user can login!! 
        echo "You have logged in!";
        
        # Our new data
        $data = array(
            'id' => $id,
            'name' => $name
        );
        # Create a connection
        $url = 'localhost:5002';
        $ch = curl_init($url);
        # Form data string
        $postString = http_build_query($data, '', '&');
        # Setting our options
        curl_setopt($ch, CURLOPT_POST, 1);
        curl_setopt($ch, CURLOPT_POSTFIELDS, $postString);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        # Get the response
        $response = curl_exec($ch);
        curl_close($ch);        
        
    } else {
        // register user
        mysqli_query($mysqli, "INSERT INTO login(name, email, password) VALUES('$name', '$email', NULL)")
            or die("Could not execute the insert query.");
        echo "You have been registered in!";
        $data = array(
            'id' => $id,
            'name' => $name
        );
        # Create a connection
        $url = 'localhost:5002';
        $ch = curl_init($url);
        # Form data string
        $postString = http_build_query($data, '', '&');
        # Setting our options
        curl_setopt($ch, CURLOPT_POST, 1);
        curl_setopt($ch, CURLOPT_POSTFIELDS, $postString);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        # Get the response
        $response = curl_exec($ch);

   

}}   
// client ID is 1038416313130-8kaejqp9740v9389dopqtrc3vqvks51c.apps.googleusercontent.com
// client secret is tuTy7QTZ9f-Nfff1M_J47ddQ


 session_start();
  ?>
 <?php
// include("connection.php");
if(isset($_POST['submit'])) {
    $user = mysqli_real_escape_string($mysqli, $_POST['username']);
    $pass = mysqli_real_escape_string($mysqli, $_POST['password']);
 
    if($user == "" || $pass == "") {
        echo "Either username or password field is empty.";
        echo "<br/>";
        echo "<a href='login.php'>Go back</a>";
    } else {
        $result = mysqli_query($mysqli, "SELECT * FROM login WHERE username='$user' AND password=md5('$pass')")
        or die("Could not execute the select query.");
        
        $row = mysqli_fetch_assoc($result);
        
        if(is_array($row) && !empty($row)) {
            $validuser = $row['username'];
            $_SESSION['valid'] = $validuser;
            $_SESSION['name'] = $row['name'];
            $_SESSION['id'] = $row['id'];
        } else {
            echo "Invalid username or password.";
            echo "<br/>";
            echo "<a href='login.php'>Go back</a>";
        }
 
        if(isset($_SESSION['valid'])) {
            header('Location: homepage.php');            
        }
    }
} 
else {
?>
    <p><font size="+2">Login</font></p>
    <form name="form1" method="post" action="">
        <table width="75%" border="0">
            <tr> 
                <td width="10%">Username</td>
                <td><input type="text" name="username"></td>
            </tr>
            <tr> 
                <td>Password</td>
                <td><input type="password" name="password"></td>
            </tr>
            <tr> 
                <td>&nbsp;</td>
                <td><input class="btn btn-outline-primary" type="submit" name="submit" value="Submit"></td>
            </tr>
        </table>
    </form>
    <?php
    echo "<a href='$auth_url'>Login Through Google </a>";
    echo "<br>";
    echo "<a href='./register.php'>Sign Up </a>";

}
?>
</body>
</html>