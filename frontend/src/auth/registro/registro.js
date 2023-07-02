import { inject, computedFrom } from 'aurelia-framework';
import { AuthService } from 'aurelia-authentication';

@inject(AuthService)
export class Registro {

  // Any signup errors will be reported by
  // giving this view model a value in the
  // catch block within the signup method
  signupError = '';

  constructor(authService) {
    this.authService = authService;
    this.nombre = '';
    this.apellidos = '';
    this.email = '';
    this.password = '';
    this.fechaNacimiento = '';
    this.tipoUsuario = '3';
  }

  signup() {
    const datosUsuario = {
      nombre: this.nombre,
      apellidos: this.apellidos,
      email: this.email,
      password: this.password,
      fechaNacimiento: this.fechaNacimiento,
      tipoUsuario: this.tipoUsuario
    };

    this.authService.signup(datosUsuario)
      .then((response) => {
        localStorage.setItem('access_token', response.access_token);
      })
      .catch(error => {
        this.signupError = error.response;
      });
  };

}
