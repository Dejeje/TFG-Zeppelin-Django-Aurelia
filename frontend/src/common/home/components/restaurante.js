import { Router } from 'aurelia-router';
import { inject } from 'aurelia-framework';
import { HttpClient } from 'aurelia-fetch-client';

@inject(Router, HttpClient)
export class Restaurante {
  router;
  http;
  listado_restaurantes = [];
  restaurantes = [];

  constructor(router, HttpClient) {
    this.router = router;
    this.http = HttpClient;

    this.fetchData();

    this.loading = false;
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

  async deleteRestaurant(id) {
    this.loading = true;
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

      const response = await this.http.delete('http://localhost:8000/zeppelin/restaurante/' + id + '/');

      this.restaurantes = this.restaurantes.filter(r => r.id !== id);
      this.detail = "Restaurante eliminado correctamente";

      this.loading = false;
    } catch (error) {
      console.error(error);
    }
  }

  goToUpdateRestaurant(id) {
    this.router.navigateToRoute('restaurante-detail', { idRestaurante: id });
  }

  newRestaurant() {
    this.router.navigateToRoute('restaurante-detail');
  }

  goToPlates(id) {
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