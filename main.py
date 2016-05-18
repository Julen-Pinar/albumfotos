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
from base64 import b64encode
import cgi
import logging
import os
import re

from google.appengine.ext import ndb
import jinja2
import webapp2
import base64

import session_module


# Jinja Environment instance necessary to use Jinja templates.
jinja_env = jinja2.Environment(
  loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
  autoescape=True)
jinja_env.filters['b64encode'] = base64.b64encode

album_key = ndb.Key('Albumfotos', 'hads1015')

class Usuarios(ndb.Model):
    usuario = ndb.TextProperty()
    contra = ndb.TextProperty()
    activo = ndb.TextProperty()
    last_touch_date_time = ndb.DateTimeProperty(auto_now_add=True)

class Albumes(ndb.Model):
    usuario = ndb.TextProperty()
    nombre = ndb.TextProperty()
    descripcion = ndb.TextProperty()
    last_touch_date_time = ndb.DateTimeProperty(auto_now_add=True)

class Fotos(ndb.Model):
    titulo = ndb.TextProperty()
    albumid = ndb.TextProperty()
    etiqueta = ndb.TextProperty()
    data = ndb.BlobProperty()
    last_touch_date_time = ndb.DateTimeProperty(auto_now_add=True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        templateBase = jinja_env.get_template("templates/base.html")
        self.response.write(templateBase.render({}))

class RegistroHandler(webapp2.RequestHandler):
    def get(self):
        templateRegistro = jinja_env.get_template("templates/registro.html")
        self.response.out.write(templateRegistro.render({}))


class Registrar (webapp2.RequestHandler):
    def post(self):
        usuarios = Usuarios(parent=album_key)
        pattern1 = re.compile("^[a-zA-Z]+\d{3}@ikasle.ehu(.es|.eus)$")
        pattern2 = re.compile("^.{6,}$")
        if not pattern1.match(self.request.get('nombre')):
            self.redirect('/reg?error=Debes proporcionar un email valido.')
            #self.response.out.write(templateRegistro.render({'error': "Debes proporcionar un email valido."}))
        elif not pattern2.match(self.request.get('contra')):
            self.redirect('/reg?error=La contrasena debe tener mas de 6 caracteres.')
            #self.response.out.write(templateRegistro.render({'error': "La contrasena debe tener mas de 6 caracteres."}))
        else:
            usuarios.usuario = self.request.get('nombre')
            usuarios.contra = self.request.get('contra')
            usuarios.activo = '0'
            usuarios.put()
            self.redirect('/?success=Registro realizado con exito.')

class Loguear (session_module.BaseSessionHandler):
    def post(self):
        usuarios = Usuarios(parent=album_key)
        lusuarios = Usuarios.query(ancestor=album_key).order(-Usuarios.last_touch_date_time)
        red = 0
        for usuarios in lusuarios:
            if cgi.escape(usuarios.usuario) == self.request.get('nombre') and cgi.escape(usuarios.contra) == self.request.get('contra') and cgi.escape(usuarios.activo) == '1':
                if self.request.get('nombre')=='admin000@ikasle.ehu.eus' or self.request.get('nombre')=='admin000@ikasle.ehu.es':
                    red = 2
                else:
                    red = 1
                    break
        if red == 1: 
            self.session['susuario'] = self.request.get('nombre')
            self.redirect('luser')
        elif red == 0:
            self.redirect('/?error=Usuario invalido o no activado.')
        elif red == 2:
            self.session['susuario'] = self.request.get('nombre')
            self.redirect('ladmin')
  
class LoginUserHandler(session_module.BaseSessionHandler):
    def get(self):
        templateUser = jinja_env.get_template("templates/user_base.html")
        lalbumes = Albumes.query(ancestor=album_key).order(-Albumes.last_touch_date_time)
        self.response.write(templateUser.render({'albumes' : lalbumes }))

class LoginAdminHandler(webapp2.RequestHandler):
    def get(self):
        templateAdminLogin = jinja_env.get_template("templates/admin_login.html")
        self.response.write(templateAdminLogin.render({}))
        
class AdminUserHandler(webapp2.RequestHandler):
    def get(self):
        templateAdminUser = jinja_env.get_template("templates/admin_user.html")
        lusuarios = Usuarios.query(ancestor=album_key).order(-Usuarios.last_touch_date_time)
        self.response.write(templateAdminUser.render({'users':lusuarios}))

class AdminAlbumHandler(webapp2.RequestHandler):
    def get(self):
        templateAdminAlbum = jinja_env.get_template("templates/admin_album.html")
        lalbumes = Albumes.query(ancestor=album_key).order(-Albumes.last_touch_date_time)
        #self.response.write("<h1>Admin: Lista de albumes </h1>  <br/><br/><a href=/ladmin>Menu Admin</a>")
        self.response.write(templateAdminAlbum.render({'albumes' : lalbumes}))
        
class CreateAlbumHandler(session_module.BaseSessionHandler):
    def post(self):
        albumes = Albumes(parent=album_key)
        albumes.usuario = self.session['susuario']
        albumes.nombre = self.request.get('nombre')
        albumes.descripcion = self.request.get('descripcion')
        albumes.put()
        self.redirect(self.request.referer)
        
class EditAlbumHandler(session_module.BaseSessionHandler):
    def get(self):
        listaFotosId = []
        album = Albumes.get_by_id(int(self.request.get_all('album')[0]), album_key)
        if not album:
            self.response.write("Error: Album no encontrado! Que andas buscando por aqui!? Aqui Blind SQL Injection no eh Juan! Aqui BLIND SQLI no! ")
        else:
            lfotos = Fotos.query(ancestor=album_key).order(-Fotos.last_touch_date_time)
            for foto in lfotos:
                if foto.albumid == str(album.key.id()):
                    logging.info("HEY")
                    listaFotosId.append(foto)
                    #image = b64encode(foto.data)
                    #self.response.out.write("<blockquote><br/>Titulo: %s</blockquote>" % cgi.escape(foto.titulo))
                    #self.response.out.write("<blockquote><br/>Etiqueta: %s</blockquote>" % cgi.escape(foto.etiqueta))
                    #self.response.headers['Content-Type'] = 'image/gif'
                    #self.response.out.write(b64encode(foto.data))
                    #self.response.out.write(foto.data.encode('base64'))
                    #img_b64 = foto.data.getvalue().encode("base64").strip()
                    #self.response.write("<img src='data:image/png;base64,%s'/>" % foto.data.encode('base64'))
            templateAlbumBase = jinja_env.get_template("templates/album_base.html")
            #self.response.write("<h1>Admin: Lista de albumes </h1>  <br/><br/><a href=/ladmin>Menu Admin</a>")
            self.response.write(templateAlbumBase.render({'album' : album, 'fotos': listaFotosId}))
            



class AddPictureHandler(webapp2.RequestHandler):
    def post(self):
        fotos = Fotos(parent=album_key)
        fotos.titulo = self.request.get('titulofoto')
        fotos.data = self.request.get('image')
        fotos.albumid = self.request.get('keyalbum')
        fotos.etiqueta = self.request.get('etiquetas')
        fotos.put()
        self.redirect(self.request.referer)

class PictureFinderHandler(session_module.BaseSessionHandler):
    def post(self):
        lfotos = Fotos.query(ancestor=album_key).order(-Fotos.last_touch_date_time)
        for foto in lfotos:
            if self.request.get('etiqueta') in foto.etiqueta:
                image = b64encode(foto.data)
                self.response.out.write("<blockquote><br/>Titulo: %s</blockquote>" % cgi.escape(foto.titulo))
                self.response.out.write("<blockquote><br/>Etiqueta: %s</blockquote>" % cgi.escape(foto.etiqueta))
                self.response.write("<img src='data:image/png;base64,%s'/>" % foto.data.encode('base64'))

class LogoutHandler(session_module.BaseSessionHandler):
    def get(self): 
        self.redirect("/")

class DeleteAlbumHandler(session_module.BaseSessionHandler):
    def post(self):
        album_entity_keyDEL = ndb.Key(urlsafe=self.request.get('entity_key'))
        album_entity_keyDEL.delete()
        self.redirect(self.request.referer)
        
class DeleteImageHandler(session_module.BaseSessionHandler):
    def post(self):
        image_entity_keyDEL = ndb.Key(urlsafe=self.request.get('entity_key'))
        image_entity_keyDEL.delete()
        self.redirect(self.request.referer)
        
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
	('/editaralbum', EditAlbumHandler),
	('/addpicture', AddPictureHandler),
	('/buscafotos', PictureFinderHandler),
    ('/logout', LogoutHandler),
    ('/deleteAlbum', DeleteAlbumHandler),
    ('/deleteImage', DeleteImageHandler),
], 	config=session_module.myconfig_dict, 
	debug=True)
