// static/js/import.js

// Helper function to display notifications
function showNotification(message, type = 'info') {
  const notification = document.createElement('div');
  notification.className = `notification ${type}`;
  notification.textContent = message;

  // Add the notification to the page
  document.body.appendChild(notification);

  // Remove the notification after 3 seconds
  setTimeout(() => {
      notification.remove();
  }, 3000);
}

// Function to handle payload deletion
function deletePayload(id) {
  if (confirm('Are you sure you want to delete this payload?')) {
      fetch(`/delete-payload/${id}`, {
          method: 'DELETE'
      })
      .then(response => response.json())
      .then(data => {
          if (data.success) {
              // Remove the row from the table only after successful deletion
              const row = document.querySelector(`tr[data-payload-id="${id}"]`);
              if (row) {
                  row.remove();
                  // Show a success message
                  showNotification('Payload deleted successfully', 'success');
              }
          } else {
              // Show error message if deletion failed
              showNotification('Failed to delete payload: ' + (data.message || 'Unknown error'), 'error');
          }
      })
      .catch(error => {
          console.error('Error deleting payload:', error);
          showNotification('An error occurred while deleting the payload', 'error');
      });
  }
}

// Function to handle file uploads
function handleFileUpload() {
  const uploadForm = document.getElementById('uploadForm');
  if (uploadForm) {
      uploadForm.addEventListener('submit', function(e) {
          e.preventDefault(); // Prevent the default form submission

          // Create FormData object from the form
          const formData = new FormData(this);

          // Send the form data using Fetch API
          fetch('/upload-endpoint', {
              method: 'POST',
              body: formData
          })
          .then(response => response.json())
          .then(data => {
              if (data.success) {
                  // Show success message
                  showNotification('File uploaded successfully!', 'success');

                  // Optionally, update the UI with the new payload
                  const payloadTable = document.querySelector('#payloadTable tbody');
                  if (payloadTable) {
                      const newRow = document.createElement('tr');
                      newRow.setAttribute('data-payload-id', data.payload.id); // Assuming the server returns the payload ID
                      newRow.innerHTML = `
                          <td>${data.payload.nama_payload}</td>
                          <td>${data.payload.jumlah_baris}</td>
                          <td>${data.payload.severity}</td>
                          <td>
                              <button onclick="deletePayload(${data.payload.id})">Delete</button>
                          </td>
                      `;
                      payloadTable.appendChild(newRow);
                  }
              } else {
                  // Show error message
                  showNotification('Error: ' + data.message, 'error');
              }
          })
          .catch(error => {
              console.error('Error:', error);
              showNotification('An error occurred while uploading the file.', 'error');
          });
      });
  } else {
      console.error('Upload form not found!');
  }
}

// Initialize the file upload functionality when the DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
  handleFileUpload();
});