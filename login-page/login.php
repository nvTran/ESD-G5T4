
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
echo "<a href='$auth_url'>Login Through Google </a>";
echo "<br>";
echo "<a href='./register.php'>Sign Up </a>";

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
//     if ($g_client->getAccessToken()){
        
//       //Get user details if user is logged in
//       $user                 = $google_oauthV2->userinfo->get();
//       $user_id              = $user['id'];
//       $user_name            = filter_var($user['name'], FILTER_SANITIZE_SPECIAL_CHARS);
//       $email                = filter_var($user['email'], FILTER_SANITIZE_EMAIL);
//       $_SESSION['email'] = $email;
//       $profile_url          = filter_var($user['link'], FILTER_VALIDATE_URL);
//       $profile_image_url    = filter_var($user['picture'], FILTER_VALIDATE_URL);
//       $personMarkup         = "$email<div><img src='$profile_image_url?sz=50'></div>";
//       $_SESSION['token']    = $gClient->getAccessToken();
// }
// else 
// {
//     //get google login url
//     $authUrl = $g_client->createAuthUrl();
// }




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
    $_SESSION['id'] = $row['id'];

    if(is_array($row) && !empty($row)) {
        // user can login!! 
        header("Location: homepage.php");
        
    } else {
        // register user
        mysqli_query($mysqli, "INSERT INTO login(name, email, password) VALUES('$name', '$email', NULL)")
            or die("Could not execute the insert query.");
        header("Location: homepage.php");
   

}

// client ID is 1038416313130-8kaejqp9740v9389dopqtrc3vqvks51c.apps.googleusercontent.com
// client secret is tuTy7QTZ9f-Nfff1M_J47ddQ


 session_start(); ?>
<html>
<head>
    <title>Login</title>
</head>
 
<body>
<a href="index.php">Home</a> <br />
<?php
include("connection.php");
 
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
} else {
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
                <td><input type="submit" name="submit" value="Submit"></td>
            </tr>
        </table>
    </form>
<?php
}}
?>
</body>
</html>