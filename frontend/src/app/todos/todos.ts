import { Component, effect, inject, OnInit, signal } from '@angular/core';
import { TodoService } from '../services/todo-service';
import { TodoModel as TodoModel } from '../models/todo.model';
import { catchError, map, pipe, throwError } from 'rxjs';
import { TodoItem } from '../components/todo-item/todo-item';
import { FormsModule } from '@angular/forms';
import { UserService } from '../services/user-service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-todos',
  imports: [TodoItem, FormsModule],
  templateUrl: './todos.html',
  styleUrl: './todos.css'
})
export class Todos implements OnInit {
  todoService = inject(TodoService);
  todoItems = signal<Array<TodoModel>>([]);
  title = signal("");
  body = signal("");

  currentUserLoggedIn = signal<boolean>(false);

  constructor(private userService: UserService, private router: Router) { 
    effect(() => {
        // Assuming _current_user is a Signal or has a getter that signals
        const userId = this.userService._current_user?.id; // Access the ID
        if (userId != null) {
            this.currentUserLoggedIn.set(true); // Update the signal
            this.loadTodos(userId); // Call the dedicated function
        } else {
            this.currentUserLoggedIn.set(false);
            let errorMessage: string = "User was not logged in. Redirecting to home";
            console.error(`${errorMessage}`);
            // throwError(() => new Error(errorMessage)); // Don't throw here, as it might crash the app
            this.router.navigate(["/"]);
        }
    });
  }


   ngOnInit(): void {
    console.log('Todos component initialized.');
  }

  loadTodos(userId: number): void {
    // console.log(this.todoService.todoItems)
    if (this.userService._current_user?.id != null) {
      this.todoService.getAllTodosFromApi()
        .pipe(catchError((err) => {
          console.log(err);
          throw err;
        }))
        .subscribe((todos) => {
          this.todoItems.set(todos);
        });
    }
    else {
      let errorMessage: string = "User was not not logged in. Redirecting to home"
      console.error(`${errorMessage}`);
      throwError(() => new Error(errorMessage))
      this.router.navigate(["/"])
    }
  };

  /**
   * Function that adds a todo to the list
   */
  onSubmitAddNote() {
    this.todoService.createTodo(this.title(), this.body()).pipe(
      catchError((err) => {
        console.log(err);
        throw err;
      })).subscribe((response) => {
    console.log(`Submitted note with id: ${response}`)
    // resetting values
    this.loadTodos(this.userService._current_user!.id)
    this.title = signal("");
    this.body = signal("");
  });
    
  };

}