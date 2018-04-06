<!DOCTYPE html>
<html lang="en">
  <head>
	  <meta charset="utf-8">
	  <meta name="viewport" content="width=device-width, initial-scale=1">
	  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
	  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>

	  <style>
		body {
		  background-color: #eee;
		}

		.form-signin {
		  max-width: 330px;
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

	  </style>
  </head>

  <body>
    <div class="container" >
      <form class="form-signin" method="post">
        <h2 class="form-signin-heading">Please sign in</h2>
        <input type="name" name="username" class="form-control" placeholder="Author name" required autofocus>
        <input type="password" name="password" class="form-control" placeholder="Password" required>
        <button class="btn btn-lg btn-primary btn-block margin" type="submit">Sign in</button>
      </form>
    </div>
  </body>
</html>
