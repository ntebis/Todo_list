import { inject, Injectable } from '@angular/core';
import { TodoModel } from '../models/todo.model';
import { HttpClient, HttpParams } from '@angular/common/http';

import { environment } from '../environment/environment';
import { UserService } from './user-service';
import { catchError, map } from 'rxjs/operators';


@Injectable({
  providedIn: 'root'
})
export class TodoService {
  private readonly baseUrl = environment.apiUrl;


  constructor(private http: HttpClient, private userService: UserService) {
    console.log("HttpClient instance injected:", this.http);
  }

  /**
   * Gets all the user notes for a user
   * @param userId The userid of the User
   * @returns An array of Todos
   */
  getAllTodosFromApi() {
    // get all notes per user
    const url = `${this.baseUrl}/user/${this.userService._current_user?.id}/notes`
    return this.http.get<Array<TodoModel>>(url)
  }


  /**
   * Function that makes the appropriate calls to create a todo note
   * @param title The title of the todo note
   * @param body The body of the todo note
   * @returns The id of the todo note
   */
  createTodo(title: string, body: string | null) {
    const url = `${this.baseUrl}/todo/`
    const params = {
      user_id: this.userService._current_user?.id,
      title: title,
      body: body
    }

    return this.http.post<number>(url, params).pipe(
      map(response => {
        console.log(`Created todo note with userId: ${params.user_id}, title: '${params.title}', body: '${params.body}' and id ${response}`);
        return response
      },
      ),
      catchError((err) => {
        console.log(`There was an error: ${err}`);
        throw err;
      })
    )
  }

  /**
   * Function that creates the api calls to edit a note
   * @param id the id of the note
   * @param title the modified title of the note
   * @param body the modified body of the note
   */
  editTodo(id: number, title: string, body: string){
    const url = `${this.baseUrl}/todo/${id}`
    const params = {
      title: title,
      body: body
    }
    return this.http.put<TodoModel>(url, params).pipe(
      map(response => {
        console.log(`Modified todo note with id ${id}, with title: '${title}' and body: '${body}'`)
      }),
      catchError((err) => {
        console.log(`There was an error: ${err}`);
        throw err;
      })
    )
  }

  deleteTodo(id: number){
    const url = `${this.baseUrl}/todo/${id}`
    return this.http.delete<TodoModel>(url).pipe(
      map(response => {
        console.log(`Deleted todo note with id: ${response.id} of user ${response.user_id}`)
      }),
      catchError((err) => {
        console.log(`There was an error: ${err}`);
        throw err;
      })
    )
  }

}