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

from google.appengine.ext import ndb

album_key = ndb.Key('Albumfotos', 'hads1015')

class Usuarios(ndb.Model):
  usuario = ndb.TextProperty()
  contra = ndb.TextProperty()


class MainHandler(webapp2.RequestHandler):
  def get(self):
    self.response.out.write("<html><body><h1>Pagina de Inicio</h1> <br/> Usuario: <br/> Contrasena: <br/><a href=reg> Registro </a> <br/><br/> <a href=luser> login user </a><br/> <a href=ladmin> login admin </a><br/>")
    lusuarios = ndb.gql('SELECT * '
                        'FROM Usuarios '
                        'WHERE ANCESTOR IS :1 ',
                        album_key)
    for usuarios in lusuarios:
      self.response.out.write("<blockquote>%s</blockquote>" % cgi.escape(usuarios.usuario))
      self.response.out.write("<blockquote>%s</blockquote>" % cgi.escape(usuarios.contra))
      self.response.out.write("</body></html>")

class RegistroHandler(webapp2.RequestHandler):
	def get(self):
		self.response.out.write("<html><body><h1>Pagina de Registro</h1><br/> Introduce los datos <br/>")
		self.response.out.write("""
			<form action="/registro" method="post">
				<div>Nombre: <textarea name="nombre" rows="1" cols="30"></textarea></div>
				<div>Contra: <textarea name="contra" rows="1" cols="30"></textarea></div>
				<div><input type="submit" value="Registrarse"></div> <br/>
				 <a href= '/'> Principal </a> <br/>
			</form>
		</body>
	</html>""")

class Registrar (webapp2.RequestHandler):
	def post(self):
		usuarios = Usuarios(parent=album_key)
		
		usuarios.usuario = self.request.get('nombre')
		usuarios.contra = self.request.get('contra')
		usuarios.put()
		self.redirect('/')
		
class LoginUserHandler(webapp2.RequestHandler):
	def get(self):
		self.response.write("<h1>Pagina de Usuario</h1> <br/> <a href= '/'> Principal </a>")
		
class LoginAdminHandler(webapp2.RequestHandler):
	def get(self):
		self.response.write("<h1>Pagina de Administrador</h1> <br/> <a href= '/'> Principal </a>")
		
class AdminUserHandler(webapp2.RequestHandler):
	def get(self):
		self.response.write("<h1>Admin: Lista de usuarios </h1>")

class AdminAlbumHandler(webapp2.RequestHandler):
	def get(self):
		self.response.write("<h1>Admin: Lista de albumes </h1>")

app = webapp2.WSGIApplication([
    ('/', MainHandler),
	('/reg', RegistroHandler),
	('/luser', LoginUserHandler),
	('/ladmin', LoginAdminHandler),
	('/auser', AdminUserHandler),
	('/aalbum', AdminAlbumHandler),
	('/registro', Registrar),
], debug=True)
