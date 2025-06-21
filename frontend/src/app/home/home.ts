import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { UserService, User } from '../services/user-service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-home',
  imports: [CommonModule, FormsModule],
  templateUrl: './home.html',
  styleUrl: './home.css'
})
export class Home {

  usernameInput: string = '';
  errorMessage: string | null = null;
  processing: boolean = false;


  constructor(private router: Router, private userService: UserService) { }


  /**
   * 
   * @returns 
   */
  onSubmit(): void {
    if (!this.usernameInput) {
      this.errorMessage = 'Please enter a username.';
      return;
    }

    this.processing = true; // Show loading indicator
    this.errorMessage = null; // Clear previous errors

    // Call the service method to get or create the user
    this.userService.getOrCreateUser(this.usernameInput)
      .subscribe({
        next: (user: User) => {
          console.log('User identified or created:', user);


          this.processing = false;
          this.router.navigate(['/todos']); // Redirect to the todo page
        },
        error: (err: Error) => {
          this.errorMessage = err.message || 'Failed to process user. Please try again.';
          this.processing = false;
          console.error('Error during user get/create:', err);
        }
      });


  }
}
