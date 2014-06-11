 <?php
require_once 'config/db_login.php';
require 'header.php';
 echo <<<_END
		<div class="container">
			<form method="POST" class="form-horizontal" role="form" action="register.php">
			
				<div class="form-group">
					<label for="email">Email address:</label>
					<input type="email" class="form-control" name="email" id="email" placeholder="you@email.com">
				</div>
				<div class="form-group">	
					<label for="carrier">Mobile carrier:</label>
					<select class="form-control" name="carrier" id="carrier">
						<option value="" disabled selected>Select your carrier</option>
						<option value="att">AT&amp;T</option>
						<option value="Verizon">Verizon</option>
						<option value="Sprint">Sprint</option>
						<option value="TMobile">T-Mobile</option>
					</select>
				</div>
				<div class="form-group">
					<label for="mobile">Mobile Phone Number:</label>
					<input type="text" class="form-control" name="mobile" id="mobile" placeholder="555-867-5309">
				</div>
				<div class="form-group">
					<label for="zip">Zipcode:</label>
					<input type="text" class="form-control" name="zip" id="zip" placeholder="01234">
				</div>

				<div class="form-group">
					<input type="submit" class="btn btn-primary btn-block"/>
				</div>
			</form>
		</div>
_END;
	$db_server = mysql_connect($db_hostname, $db_username, $db_password);
	
	if(!$db_server) die("unable to connect to mySql: " . mysql_error());

	mysql_select_db($db_database)
		or die("unable to select datebase: " . mysql_error());
	

	if (isset($_POST['email']))
	{
		$email = sanitizeString($_POST['email']);
		$zip = sanitizeString($_POST['zip']);
		$mobile = sanitizeString($_POST['mobile']);
		$now = date('Y-m-d H:i:s');
		$carrier = sanitizeString($_POST['carrier']);
		$result = mysql_query("select carrier_id from carrier_lkp where name = '$carrier'");
		$carrier_id = mysql_result($result,0);
		
		$userExists = mysql_query("select mobile, user_id from users where mobile = '$mobile'");
		if(mysql_num_rows($userExists))
		{
			$user_id = mysql_result($userExists,0,"user_id");
			mysql_query("INSERT INTO zipsForUser (user_id, zipcode,isActive,querytime) VALUES('$user_id', '$zip', 1, 400)");
		}
		else
		{
			mysql_query("INSERT INTO users (email, addedDate, updateDate, mobile, carrier_id) VALUES('$email', '$now', '$now', '$mobile', '$carrier_id')");
			mysql_query("INSERT INTO zipsForUser (user_id, zipcode,isActive) VALUES(LAST_INSERT_ID(), '$zip', 1)");	
		}
	}
 
	mysql_close($db_server);
	
	function sanitizeString($var)
	{
		$var = strip_tags($var);
		$var = htmlentities($var);
		$var = stripslashes($var);
		return mysql_real_escape_string($var);
	}
	
echo <<<_END
	</body>
	</html>
_END;
 ?>