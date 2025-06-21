import { Component, inject, OnInit, signal } from '@angular/core';
import { TodoService } from '../services/todo-service';
import { Todo as TodoModel } from '../models/todo.model';
import { catchError, pipe } from 'rxjs';
import { TodoItem } from '../components/todo-item/todo-item';
import { FormsModule } from '@angular/forms';
import { UserService } from '../services/user-service';

@Component({
  selector: 'app-todos',
  imports: [TodoItem, FormsModule, UserService],
  templateUrl: './todos.html',
  styleUrl: './todos.scss'
})
export class Todos implements OnInit {
  todoService = inject(TodoService);
  todoItems = signal<Array<TodoModel>>([])
  searchTerm = signal("")

  constructor(private userService:UserService) {}

  ngOnInit(): void {
    // console.log(this.todoService.todoItems)
    this.todoService.getAllTodosFromApi(this.userService._current_user?.id)
      .pipe(catchError((err) => {
        console.log(err);
        throw err;

      }))
      .subscribe((todos) => {
        this.todoItems.set(todos);
      });
  }

  updateTodoItem(todoItem: TodoModel){
    this.todoItems.update((todos) => {
      return todos.map(todo => {
        if (todo.id == todoItem.id){
          return{
            ...todo,
            completed: !todo.completed,
          }
        }
        return todo;
      })
    })
  }
}