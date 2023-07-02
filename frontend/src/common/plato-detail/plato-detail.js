import { Router, activationStrategy  } from 'aurelia-router';
import { inject } from 'aurelia-framework';
import { HttpClient, json } from 'aurelia-fetch-client';

@inject(Router, HttpClient)
export class PlatoDetail {
    loading = true;
    idPlato = null;
    router;
    plato = {
        titulo: '',
        descripcion: '',
        disponibilidad: 0,
        precio: 0
    }

    activate(params) {
        this.idPlato = params.idPlato;
        this.idRestaurante = params.idRestaurante;

        if (this.idPlato)
            this.fetchPlato(this.idPlato);
        else
            this.loading = false;
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

    async updatePlato() {
        this.loading = true;

        this.plato.restaurante = this.idRestaurante;

        try {
            if (this.idPlato) {
                var response = await this.http.patch('http://localhost:8000/zeppelin/plato/' + this.idPlato + '/', json(this.plato));
            } else {
                var response = await this.http.post('http://localhost:8000/zeppelin/plato/', json(this.plato));
            }
            const data = await response.json();

            this.detail = data.detail;

            this.loading = false;
        } catch (error) {
            console.error(error);
        }

        this.router.navigateBack()
    }

    async fetchPlato(id) {
        try {
            const response = await this.http.fetch('http://localhost:8000/zeppelin/plato/' + id + '/');
            const data = await response.json();

            this.plato = data;

            this.loading = false;
        } catch (error) {
            console.error(error);
        }
    }
}