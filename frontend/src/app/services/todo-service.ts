import { inject, Injectable } from '@angular/core';
import { Todo } from '../models/todo.model';
import { HttpClient, HttpParams } from '@angular/common/http';

import { environment } from '../environment/environment';


@Injectable({
  providedIn: 'root'
})
export class TodoService {
  private readonly baseUrl = environment.apiUrl;


  constructor(private http: HttpClient) { 
    console.log("HttpClient instance injected:", this.http);
  }
  
  /**
   * Gets all the user notes for a user
   * @param userId The userid of the User
   * @returns An array of Todos
   */
  getAllTodosFromApi(userId: number){
    // get all notes per user
    const url = `${this.baseUrl}/user/${userId}/notes`
    return this.http.get<Array<Todo>>(url)
  }



}

