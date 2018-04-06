<!DOCTYPE html>

<html>
  <head>
		<meta charset="utf-8">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
		<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
		<title>Sign Up</title>
		<style type="text/css">

		.form-signin {
		  max-width: 550px;
		  padding: 15px;
		  margin: auto;
		}

		.form-signin .form-control {
		  height: auto;
		  padding: 10px;
		  font-size: 16px;
		}
		.margin{
			margin-top: 10px;
		}

		.margin{
			margin: auto;
		}
		.fixedmargin{
			margin-top: 5px;
		}
		.error {
			color: red;
		}
		</style>
	</head>

	<body>
		<div class="container text-center">
			<h1>Signup</h1>

			<div class="jumbotron">
				<form method="post">
					<table class="margin">
						<tr>
							<td><b>Username</b></td>
							<td><input type="text" name="username" class="form-control"  value="{{username}}" required autofocus></td>
							<td class="error">{{username_error}}</td>
						</tr>

						<tr>
							<td><b>Password</b></td>
							<td><input type="password" name="password" class="form-control" required></td>
							<td class="error">{{password_error}}</td>
						</tr>

						<tr>
							<td><b>Verify Password</b></td>
							<td><input type="password" name="verify" class="form-control"  required></td>
							<td class="error">{{verify_error}}</td>
						</tr>

						<tr>
							<td><b>Email (optional)</b></td>
							<td><input type="text" name="email" value="{{email}}" class="form-control"  ></td>
							<td class="error">{{email_error}}</td>
						</tr>

						<tr>
							<td></td>
							<td><button class="btn btn-lg btn-primary text-center btn-block fixedmargin" type="submit">Submit</button></td>
							<td></td>
						</tr>
					</table>
				</form>
			</div>
		</div>




	</body>

</html>
