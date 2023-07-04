import { HttpClient } from 'aurelia-fetch-client';
import { inject } from 'aurelia-framework';

@inject(HttpClient)
export class ValidarUsuarios {
   usuarios = undefined;
   loading = true;
   http;

    constructor(HttpClient) {
        this.http = HttpClient;
        this.fetchData();    
    }

    async validateUser(id) { 
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

            const response = await this.http.fetch('http://localhost:8000/zeppelin/usuario/validar/'+id+'/');
            const data = await response.json();

            this.usuarios = this.usuarios.filter(usuario => usuario.id !== id);
            
            this.detail = data.detail;
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
    
          const response = await this.http.fetch('http://localhost:8000/zeppelin/usuario/por_validar/');
          const data = await response.json();
          
          this.usuarios = data;
          this.loading = false;
        } catch (error) {
          console.error(error);
        }
      }
}