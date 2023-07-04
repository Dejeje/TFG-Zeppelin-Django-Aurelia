import { AuthService, FetchConfig } from 'aurelia-authentication';
import { Router } from 'aurelia-router';
import { inject } from 'aurelia-framework';
import { HttpClient } from 'aurelia-fetch-client';

@inject(AuthService, Router, HttpClient)
export class Client {
  user = undefined;
  loading = true;
  router;
  http;
  listado_restaurantes = [];
  restaurantes = [];

  constructor(authService, router, HttpClient) {
    this.authService = authService;
    this.router = router;
    this.http = HttpClient;

    this.authService.getMe()
      .then(profile => {
        this.user = profile;
        this.loading = false;
      })
      .catch(err => {
        console.log("home failure " + err);
      });

    this.fetchData();
  }

  filterCategories(value) {
    if (!value) {
      this.restaurantes = this.listado_restaurantes;
    }
    this.restaurantes = this.listado_restaurantes.filter(x => {
      return x.nombre.toLowerCase().trim().includes(value.toLowerCase().trim()) || x.categorias.some(c => {
        return c.categoria.toLowerCase().trim().includes(value.toLowerCase().trim())
      });
    });
  }

  goToValidateUsers() {
    this.router.navigateToRoute('validate-users');
  }

  goToPlatos(id) {
    this.router.navigateToRoute('platos', { idRestaurante: id });
  }

  async fetchData() {
    try {
      var token;
      localStorage.getItem('access_token', token);

      this.http.configure(config => {
        config.withDefaults({
          headers: {
            'Content-Type': 'application/json; charset=UTF-8',
            Authorization: `Token ${token}`
          }
        });
      });

      const response = await this.http.fetch('http://localhost:8000/zeppelin/restaurante/');
      const data = await response.json();

      this.listado_restaurantes = data;
      this.restaurantes = data;
    } catch (error) {
      console.error(error);
    }
  }
}