import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';

import { environment } from '../environment/environment';
import { catchError, map, tap } from 'rxjs/operators';
import { throwError } from 'rxjs/internal/observable/throwError';
import { Observable } from 'rxjs';

export interface User {
  id: number;
  username: string;
}

@Injectable({
  providedIn: 'root'
})
export class UserService {
  private readonly baseUrl = environment.apiUrl;
  _current_user: User | null = null;

  constructor(private http: HttpClient) {
    console.log("HttpClient instance injected:", this.http);
  }

  /**
   * Function that creates or gets a user id based on a username
   * This is to demonstrate basic user handling
   * @param username The username of the user
   * @returns Product
   */
  getOrCreateUser(username: string): Observable<User> {
    // in hindsight i should have created the api to do that but now will just implement it here
    const userUrl = `${this.baseUrl}/user/`
    const params = {
      "username": username
    }

    return this.http.get<{ id: number }>(userUrl, { params }).pipe(
      map(response => {
        console.log(`User ID found for username '${username}': ${response.id}`);
        this._current_user = { id: response.id, username: username };
        return this._current_user;
      }),
      catchError((error: HttpErrorResponse) => {
        // if user not found create them
        if (error.status === 404) {
          console.log(`User with username '${username}' not found (404). Attempting to create new user.`);
          return this.http.post<User>(userUrl, params).pipe(
            tap(newUser => console.log('New user created successfully:', newUser.username, 'ID:', newUser.id)),
            catchError(postError => {
              console.error(`Error creating user '${username}':`, postError);
              return this.handleError(postError);
            })
          );
        } else {
          console.error(`Error identifying user by username '${username}':`, error);
          return this.handleError(error);
        }
      })
    );
  }


  private handleError(error: HttpErrorResponse): Observable<never> {
    let errorMessage = 'An unknown error occurred!';
    console.error(`HTTP Error: ${errorMessage}`);
    return throwError(() => new Error(errorMessage));
  }
}
