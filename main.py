#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import cgi
import re
import session_module

from google.appengine.ext import ndb
from webapp2_extras import sessions

album_key = ndb.Key('Albumfotos', 'hads1015')

class Usuarios(ndb.Model):
  usuario = ndb.TextProperty()
  contra = ndb.TextProperty()
  activo = ndb.TextProperty()

class Albumes(ndb.Model):
  usuario = ndb.TextProperty()
  nombre = ndb.TextProperty()

class Fotos(ndb.Model):
  titulo = ndb.TextProperty()
  albumid = ndb.TextProperty()
  etiqueta = ndb.TextProperty()
  data = ndb.TextProperty()


class MainHandler(webapp2.RequestHandler):
  def get(self):
    self.response.out.write("<html><body><h1>Pagina de Inicio</h1><br/><br/>")
    #lusuarios = ndb.gql('SELECT * '
                        #'FROM Usuarios '
                        #'WHERE ANCESTOR IS :1 ',
                        #album_key)
    #for usuarios in lusuarios:
      #self.response.out.write("<blockquote>%s</blockquote>" % cgi.escape(usuarios.usuario))
      #self.response.out.write("<blockquote>%s</blockquote>" % cgi.escape(usuarios.contra))
    self.response.out.write("""
			<form action="/logueo" method="post">
				<div>Email: <textarea name="nombre" rows="1" cols="30"></textarea></div>
				<div>Contrasena: <textarea name="contra" rows="1" cols="30"></textarea></div>
				<div><input type="submit" value="Login"></div> <br/>
				 <a href=reg> Registro </a> <br/>
			</form>
		</body>
	</html>""")

class RegistroHandler(webapp2.RequestHandler):
	def get(self):
		self.response.out.write("<html><body><h1>Pagina de Registro</h1><br/> Introduce los datos <br/>")
		self.response.out.write("""
			<form action="/registro" method="post">
				<div>Email: <textarea name="nombre" rows="1" cols="30"></textarea></div>
				<div>Contra: <textarea name="contra" rows="1" cols="30"></textarea></div>
				<div><input type="submit" value="Registrarse"></div> <br/>
				 <a href= '/'> Principal </a> <br/>
			</form>
		</body>
	</html>""")

class Registrar (webapp2.RequestHandler):
	def post(self):
		usuarios = Usuarios(parent=album_key)
		pattern1 = re.compile("^[a-zA-Z]+\d{3}@ikasle.ehu(.es|.eus)$")
		pattern2 = re.compile("^.{6,}$")
		if not pattern1.match(self.request.get('nombre')):
		  self.response.out.write("Debes proporcionar un email valido.")
		  self.response.write(" <br/> <a href= reg> Volver al registro </a>")
		elif not pattern2.match(self.request.get('contra')):
		  self.response.out.write("La contrasena debe tener mas de 6 caracteres.")
		  self.response.write(" <br/> <a href= reg> Volver al registro </a>")
		else:
		 usuarios.usuario = self.request.get('nombre')
		 usuarios.contra = self.request.get('contra')
		 usuarios.activo = '0'
		 usuarios.put()
		 self.redirect('/')
		
class Loguear (session_module.BaseSessionHandler):
	def post(self):
		#self.session_store = sessions.get_store(request=self.request)
		usuarios = Usuarios(parent=album_key)
		#lusuarios = ndb.gql('SELECT * '
        #                'FROM Usuarios '
        #                'WHERE ANCESTOR IS :1 ',
        #                album_key)
		lusuarios = Usuarios.query()
		red = 0
		for usuarios in lusuarios:
		  if cgi.escape(usuarios.usuario) == self.request.get('nombre') and cgi.escape(usuarios.contra) == self.request.get('contra') and cgi.escape(usuarios.activo) == '1':
		    if self.request.get('nombre')=='admin000@ikasle.ehu.es':
		      red = 2
		    else:
		      red = 1
		    break
		if red == 1: 
		  self.session['susuario'] = self.request.get('nombre')
		  self.redirect('luser')
		elif red == 0:
		  self.response.out.write("red 0")
		elif red == 2:
		  #self.session['susuario'] = self.request.get('nombre')
		  self.redirect('ladmin')
		  
class LoginUserHandler(session_module.BaseSessionHandler):
	def get(self):
		self.response.write("<html><body><h1>Pagina de Usuario</h1> <br/>")
		lalbumes = Albumes.query()
		for albumes in lalbumes:
		  if albumes.usuario == self.session['susuario']:
		    self.response.out.write("<blockquote>%s</blockquote>" % cgi.escape(albumes.usuario))
		    self.response.out.write("<blockquote>%s</blockquote>" % cgi.escape(albumes.nombre))
		    
		self.response.write("<a href= '/'> Principal </a>")
		self.response.out.write("""
			<form action="/crearAlbum" method="post">
				<div>Nombre del album: <textarea name="nombrealbum" rows="1" cols="30"></textarea></div>
				<div><input type="submit" value="Anadir album"></div> <br/>
			</form>
		</body>
	</html>""")
		
class LoginAdminHandler(webapp2.RequestHandler):
	def get(self):
		self.response.write("<h1>Pagina de Administrador</h1> <br/> <a href=/auser> Gestionar Usuarios </a> <br/> <a href=/aalbum> Gestionar albumes </a> <br/> <a href= '/'> Principal </a>")
		
class AdminUserHandler(webapp2.RequestHandler):
	def get(self):
		self.response.write("<html><body><h1>Admin: Lista de usuarios </h1> <br/><br/><a href=/ladmin>Menu Admin</a>")
		lusuarios = Usuarios.query()
		for usuarios in lusuarios:
		  self.response.out.write("<blockquote>%s</blockquote>" % cgi.escape(usuarios.usuario))
		  self.response.out.write("<blockquote>%s</blockquote>" % cgi.escape(usuarios.contra))
		  self.response.out.write("<blockquote>%s</blockquote>" % cgi.escape(usuarios.activo))
		  self.response.out.write("""
			<form action="/activar" method="post">
				<!--<div>Usuario a Activar: <textarea name="anombre" rows="1" cols="30"></textarea></div>-->
				<div><input type="submit" value="Activar"></div> <br/>
			</form>
			<form action="/borrarUsuario" method="post">
				<!--<div>Usuario a Borrar: <textarea name="bnombre" rows="1" cols="30"></textarea></div>-->
				<div><input type="submit" value="Borrar"></div> <br/>
			</form>
		</body>
	</html>""")

class AdminAlbumHandler(webapp2.RequestHandler):
	def get(self):
		self.response.write("<h1>Admin: Lista de albumes </h1>  <br/><br/><a href=/ladmin>Menu Admin</a>")
		
class CreateAlbumHandler(webapp2.RequestHandler):
	def post(self):
		albumes = Albumes(parent=album_key)
		albumes.usuario = self.session['susuario']
		albumes.nombre = self.request.get('nombrealbum')
		albumes.put()
		self.redirect('luser')

app = webapp2.WSGIApplication([
    ('/', MainHandler),
	('/reg', RegistroHandler),
	('/luser', LoginUserHandler),
	('/ladmin', LoginAdminHandler),
	('/auser', AdminUserHandler),
	('/aalbum', AdminAlbumHandler),
	('/registro', Registrar),
	('/logueo', Loguear),
	('/crearAlbum', CreateAlbumHandler),
], 	config=session_module.myconfig_dict, 
	debug=True)
