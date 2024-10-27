// src/services/userService.js

// Import the base URL from config.js instead of defining it here
import { API_BASE_URL } from "../config"; // Import base API URL

// Function to fetch user profile
export async function getUserProfile() {
  try {
    const response = await fetch(`${API_BASE_URL}/user/profile`, { // Use imported API_BASE_URL
      method: "GET",
      credentials: "include", // Important for session-based auth
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) throw new Error("Failed to fetch user profile");
    const userData = await response.json();
    return userData;
  } catch (error) {
    console.error(error);
    return null;
  }
}

// Function to save a QR code
export async function saveQRCode(inputText, qrImage) {
  try {
    const response = await fetch(`${API_BASE_URL}/user/save-qr`, { // Use imported API_BASE_URL
      method: "POST",
      credentials: "include", // Important for session-based auth
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ inputText, qrImage }),
    });

    if (!response.ok) throw new Error("Failed to save QR code");
    return await response.json();
  } catch (error) {
    console.error(error);
  }
}

// Function to delete a QR code by its ID
export async function deleteQRCode(id) {
  try {
    const response = await fetch(`${API_BASE_URL}/user/delete-qr/${id}`, { // Use imported API_BASE_URL
      method: "DELETE",
      credentials: "include", // Important for session-based auth
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) throw new Error("Failed to delete QR code");
    return await response.json();
  } catch (error) {
    console.error(error);
    throw error;
  }
}

// Function to log out a user
export async function logoutUser(setUser) {
  try {
    const response = await fetch(`${API_BASE_URL}/user/logout`, { // Use imported API_BASE_URL
      method: "POST",
      credentials: "include", // Important for session-based auth
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (response.ok) {
      setUser(null); // Reset user state in App after logging out
    } else {
      console.error("Failed to log out");
    }
  } catch (error) {
    console.error(error);
  }
}

// Function to get generated QR codes for the logged-in user
export async function getGeneratedQRCodes() {
  try {
    const response = await fetch(`${API_BASE_URL}/user/qr-codes`, { // Use imported API_BASE_URL
      method: "GET",
      credentials: "include", // Important for session-based auth
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) throw new Error("Failed to fetch QR codes");
    const qrCodes = await response.json();
    return qrCodes;
  } catch (error) {
    console.error(error);
    return [];
  }
}

// Function to handle user login
export async function loginUser(email, password) {
  try {
    const response = await fetch(`${API_BASE_URL}/login`, { // Use imported API_BASE_URL
      method: "POST",
      credentials: "include", // Important for session-based auth
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email, password }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "Failed to log in");
    }

    return data; // This should contain { message, user }
  } catch (error) {
    console.error(error);
    throw error;
  }
}

// Function to handle user signup
export async function signupUser(name, email, password) {
  try {
    const response = await fetch(`${API_BASE_URL}/register`, { // Use imported API_BASE_URL
      method: "POST",
      credentials: "include", // Important for session-based auth
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ name, email, password }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "Failed to sign up");
    }

    return data; // This should contain { message, user }
  } catch (error) {
    console.error(error);
    throw error;
  }
}

// Update user profile
export async function updateProfile(name, email, currentPassword, newPassword) {
  try {
    const response = await fetch(`${API_BASE_URL}/user/update-profile`, { // Use imported API_BASE_URL
      method: "POST",
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ name, email, current_password: currentPassword, new_password: newPassword }),
    });

    if (!response.ok) throw new Error("Failed to update profile");
    return await response.json();
  } catch (error) {
    console.error(error);
    throw error;
  }
}

// Delete user account with password confirmation
export async function deleteAccount(password) {
  try {
    const response = await fetch(`${API_BASE_URL}/user/delete-account`, { // Use imported API_BASE_URL
      method: "DELETE",
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ password }), // Send the password
    });

    if (!response.ok) throw new Error("Failed to delete account");
    return await response.json();
  } catch (error) {
    console.error(error);
    throw error;
  }
}
