<!DOCTYPE html>
<html>
<head>
<title >Blog</title>
</head>
<body>

%if (username != None):
Welcome {{username}}        <a href="/logout">Logout</a> | <a href="/newpost">New Post</a><p>
<a href = /authorspecific> See Mine Only </a>
%else :
<a href = /signup>Signup for new authors</a>
<a href = /login>Existing authors login</a>
%end

<h1 style="background-color:DodgerBlue;">My Blog</h1>

%for post in myposts:
<h2><a href="/post/{{post['permalink']}}">{{post['title']}}</a></h2>
Posted {{post['post_date']}} <i>By {{post['author']}}</i><br>
<hr>
{{!post['body']}}
<p>
<p>
<em>Filed Under</em>:
%if ('tags' in post):
%for tag in post['tags'][0:1]:
{{tag}}
%for tag in post['tags'][1:]:
, {{tag}}
%end
%end

<p>
%end


</body>
</html>


