import { AuthService } from 'aurelia-authentication';
import { Router } from 'aurelia-router';
import { inject } from 'aurelia-framework';
import { HttpClient, json } from 'aurelia-fetch-client';

@inject(AuthService, Router, HttpClient)
export class Platos {
    platos = [];
    idRestaurante = undefined;
    user = undefined;
    authService;
    loading = true;
    router;
    http;

    activate(params) {
        this.idRestaurante = params.idRestaurante;
        this.fetchData();
    }

    constructor(authService, router, HttpClient) {
        this.authService = authService;
        this.router = router;
        this.http = HttpClient;

        this.authService.getMe()
            .then(profile => {
                this.user = profile;});

    }
    
    getTipoUsuario(idTipo) {
        switch (idTipo) {
            case 2: return 'Restaurante';
            case 3: return 'Cliente';
            default: return 'Admin';
        }
    }

    async changestatusPlate(id, status) {
        var index = this.platos.findIndex(p => p.id == id);

        if (index !== -1) {
            this.platos[index].disponibilidad = status;
        }

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
           
            var response = await this.http.patch('http://localhost:8000/zeppelin/plato/' + id + '/', json(this.platos[index]));
            const data = await response.json();

            this.detail = data.detail;
        } catch (error) {
            console.error(error);
        }
    }

    goToUpdatePlate(id) {
        this.router.navigateToRoute('plato-detail', { idPlato: id, idRestaurante: this.idRestaurante });
    }

    newPlate() {
        this.router.navigateToRoute('plato-detail', { idRestaurante: this.idRestaurante });
    }

    async deletePlate(id) {
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

            const response = await this.http.delete('http://localhost:8000/zeppelin/plato/'+id+'/');

            this.platos = this.platos.filter(p => p.id !== id);
            this.detail = "Plato eliminado correctamente";

            this.loading = false;
          } catch (error) {
            console.error(error);
          }    
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

            const response = await this.http.fetch('http://localhost:8000/zeppelin/restaurante/' + this.idRestaurante + '/platos/');
            const data = await response.json();

            this.platos = data;

            let plato = localStorage.getItem('nombreVariable');
            
            if (plato !== null) {
                
              }

            this.loading = false;
        } catch (error) {
            console.error(error);
        }
    }
}