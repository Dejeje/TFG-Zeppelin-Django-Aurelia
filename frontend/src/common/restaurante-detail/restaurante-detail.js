import { Router } from 'aurelia-router';
import { inject } from 'aurelia-framework';
import { HttpClient, json } from 'aurelia-fetch-client';

@inject(Router, HttpClient)
export class RestaurantDetail {
    loading = true;
    id = null;
    restaurante = {
        nombre: '',
        categorias: [],
        direccion: {
            calle: '',
            numero: 0,
            ciudad: '',
            codigoPostal: 0
        }
    }

    activate(params) {
        this.idRestaurante = params.idRestaurante;
        
        if (this.idRestaurante) 
            this.fetchRestaurante(this.idRestaurante);
        else 
            this.fetchCategorias();
    }

    constructor(router, HttpClient) {
        this.router = router;
        this.http = HttpClient;

        var token = localStorage.getItem('access_token');

        this.http.configure(config => {
            config.withDefaults({
                headers: {
                    Authorization: `Token ${token}`
                }
            });
        });
    }

    async updateRestaurant() {
        var token = localStorage.getItem('access_token', token);

        this.http.configure(config => {
            config.withDefaults({
                headers: {
                    'Content-Type': 'application/json; charset=UTF-8',
                    Authorization: `Token ${token}`
                }
            });
        });

        try {
            if (this.idRestaurante) {
                var response = await this.http.patch('http://localhost:8000/zeppelin/restaurante/' + this.idRestaurante + '/', json(this.restaurante));
            } else {
                var response = await this.http.post('http://localhost:8000/zeppelin/restaurante/', json(this.restaurante));
            }

            const data = await response.json();

            this.detail = data.detail;
        } catch (error) {
            console.error(error);
        }
    }

    async fetchRestaurante(id) {
        try {
            const response = await this.http.fetch('http://localhost:8000/zeppelin/restaurante/' + id + '/');
            const data = await response.json();

            this.restaurante = data;

            this.restaurante.categorias = this.restaurante.categorias.map(y => y.id);

            this.fetchCategorias();
        } catch (error) {
            console.error(error);
        }
    }

    async fetchCategorias() {
        try {
            const response = await this.http.fetch('http://localhost:8000/zeppelin/categoria/');
            const data = await response.json();

            this.categorias = data;
            
            this.loading = false;
        } catch (error) {
            console.error(error);
        }
    }

}
