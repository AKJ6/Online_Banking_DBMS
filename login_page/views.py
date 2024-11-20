from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth import update_session_auth_hash
from datetime import datetime
from django.contrib import messages
from decimal import Decimal
from decimal import Decimal, InvalidOperation 
# Login view
from decimal import Decimal, ROUND_DOWN
def show_accounts(request):
    users = get_user_model().objects.exclude(id=request.user.id)  # Exclude the logged-in user
    return render(request, 'show_accounts.html', {'users': users})

# View to handle fund transfer
def fund_transfer(request, receiver_id):
    receiver = get_user_model().objects.get(id=receiver_id)  # Get the receiver's account
    
    if request.method == 'POST':
        amount = request.POST.get('amount')

        try:
            # Convert amount to Decimal and ensure it's greater than zero
            if not amount or Decimal(amount) <= 0:
                messages.error(request, "Please enter a valid amount.")
                return redirect('fund_transfer', receiver_id=receiver.id)
            
            amount = Decimal(amount)  # Convert to Decimal
            
            # Check if the sender has enough balance
            if request.user.balance < amount:
                messages.error(request, "Insufficient balance.")
                return redirect('fund_transfer', receiver_id=receiver.id)

            # Perform the fund transfer: deduct from sender and add to receiver
            request.user.balance -= amount
            receiver.balance += amount
            
            # Save the updated balances
            request.user.save()
            receiver.save()

            messages.success(request, f"Successfully transferred ₹{amount} to {receiver.username}")
            return redirect('home')  # Redirect to home or any other page after successful transfer
        
        except (ValueError, InvalidOperation):
            messages.error(request, "Invalid amount entered. Please enter a numeric value.")
            return redirect('fund_transfer', receiver_id=receiver.id)

    return render(request, 'fund_transfer.html', {'receiver': receiver})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            
            # Check if the user's balance is below 5000
            if user.balance < 5000:
                messages.error(request, "Error: Amount less than minimum balance. Login failed.")
                return redirect('login')  # Redirect back to the login page if balance is insufficient

            # If balance is sufficient, log the user in
            login(request, user)
            return home_view(request)  # Redirect to the home view after successful login
    else:
        form = AuthenticationForm()

    return render(request, 'login/login.html', {'form': form})


    return render(request, 'login/login.html', {'form': form})

# Home view
def home_view(request):
    # Access the balance field of the logged-in user
    balance = request.user.balance  # Access the balance of the currently logged-in user
    username = request.user.username  # Access the username
    email = request.user.email  # Access the email
    loan= request.user.loan_amount
    # Get the current year dynamically (for footer)
    current_year = datetime.now().year

    # Render the home page with user and balance information
    return render(request, 'home.html', {
        'username': username, 
        'email': email,
        'balance': balance, 
        'current_year': current_year,
        'loan':loan
    })

def edit_profile(request):
    if request.method == 'POST':
        # Check if the request includes the data to update username, email, and password
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = request.user

        # Update username and email
        if username:
            user.username = username
        if email:
            user.email = email

        # Update password if provided
        if password:
            user.set_password(password)

        # Save the updated user object
        user.save()

        # Update the session authentication hash to prevent logout when changing password
        update_session_auth_hash(request, user)

        return home_view(request)  # Redirect to home after the update

    return render(request, 'edit_profile.html', {'user': request.user})
from django.shortcuts import render, redirect
from django.contrib import messages
from decimal import Decimal, ROUND_DOWN  # Import ROUND_DOWN for rounding

def loan_request(request):
    user_balance = request.user.balance  # Get the user's current balance
    
    # Calculate the maximum loan amount (30% of balance)
    max_loan_amount = user_balance * Decimal(0.30)

    if request.method == 'POST':
        # Get the requested loan amount from the form input
        requested_loan = request.POST.get('loan_amount')

        try:
            requested_loan = Decimal(requested_loan)  # Convert to Decimal
            
            # Round the requested loan amount to 2 decimal places
            requested_loan = requested_loan.quantize(Decimal('0.01'), rounding=ROUND_DOWN)

            # Check if the requested loan amount is within the limit
            if requested_loan > max_loan_amount:
                messages.error(request, f"Sorry, you can only request up to ₹{max_loan_amount} as loan (30% of your balance).")
                return redirect('loan_request')  # Redirect back to the loan request page if invalid

            # Add the loan amount to the user's balance
            request.user.balance += requested_loan  # Increase balance by the loan amount
            request.user.loan_amount += requested_loan  # Assuming you have a loan_amount field in your model to track loans

            # Save the updated user object
            request.user.save()

            # Show success message
            messages.success(request, f"Your loan request for ₹{requested_loan} has been approved. Your new balance is ₹{request.user.balance}.")
            return redirect('home')  # Redirect to home page after successful loan request

        except (ValueError, InvalidOperation):
            messages.error(request, "Please enter a valid loan amount.")
            return redirect('loan_request')  # Redirect back to the loan request page if invalid input

    # Render the loan request page with the max loan amount
    return render(request, 'loan_request.html', {'max_loan_amount': max_loan_amount})
