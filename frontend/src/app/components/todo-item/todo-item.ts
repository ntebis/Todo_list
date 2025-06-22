import { Component, input, signal, NgModule } from '@angular/core';
import { TodoModel } from '../../models/todo.model';
import { HttpClient } from '@angular/common/http';
import { UserService } from '../../services/user-service';

import { TodoService } from '../../services/todo-service';
import { FormsModule } from '@angular/forms';
import { Todos } from '../../todos/todos';
import { catchError } from 'rxjs';

@Component({
  selector: 'app-todo-item',
  imports: [FormsModule],
  templateUrl: './todo-item.html',
  styleUrl: './todo-item.css'
})
export class TodoItem {

  todo = input.required<TodoModel>();
  isEditing: boolean = false;
  editedTitle = signal('');
  editedBody = signal('');
  // editedTitle = '';
  // editedBody = '';

  constructor(
    private http: HttpClient,
    private userService: UserService, 
    private todoService: TodoService, 
    private todosComponent: Todos) { };

  
  /**
   * Function that edits note
   */
  onEditClick(): void {

    this.isEditing = true;
    this.editedTitle = signal(this.todo().title);
    this.editedBody = signal(this.todo().body);
    // this.editedTitle = this.todo().title;
    // this.editedBody = this.todo().body;
    console.log('Edit mode entered for:', this.todo());
  }


  /**
   * Function to update the note 
   */
  onSaveClick(): void {


    // console.log('Saving changes:', updatedTodo);
    this.todoService.editTodo(this.todo().id, this.editedTitle(), this.editedBody()).pipe(
          catchError((err) => {
            console.log(err);
            throw err;
          })).subscribe(() => {
        console.log(`Edited note with id: ${this.todo().id}`)
        this.todosComponent.loadTodos(this.userService._current_user!.id) // reload the todos list with the latest data
        this.isEditing = false;
      })
  }

  onCancelClick(): void {
    this.isEditing = false;
  }

  onClickDelete() {
    this.todoService.deleteTodo(this.todo().id).pipe(
      catchError((err) => {
            console.log(err);
            throw err;
          })
    ).subscribe(() => {
      console.log(`Removed note with id: ${this.todo().id}`)
      this.todosComponent.loadTodos(this.userService._current_user!.id) // reload the todos list with the latest data
    })
  }
}
