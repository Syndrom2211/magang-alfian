$(document).ready(function() {
    $('#searchInput').on('keyup', function() {
        var value = $(this).val().toLowerCase();
        $('#attackLogsTable tbody tr').filter(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });

    $('.pagination a').on('click', function(e) {
        e.preventDefault();
        $('.pagination li').removeClass('active');
        $(this).parent().addClass('active');
    });

    var rowsPerPage = 10;
    var currentPage = 1;
    var $table = $('#attackLogsTable');
    var $rows = $table.find('tbody tr');
    var totalRows = $rows.length;
    var totalPages = Math.ceil(totalRows / rowsPerPage);

    function updatePagination() {
        $('.pagination').empty();
        $('.pagination').append('<li><a href="#" class="prev">Previous</a></li>');
        for (var i = 1; i <= totalPages; i++) {
            $('.pagination').append('<li><a href="#">' + i + '</a></li>');
        }
        $('.pagination').append('<li><a href="#" class="next">Next</a></li>');
        $('.pagination li').eq(currentPage).addClass('active');
    }

    function showPage(page) {
        currentPage = page;
        var start = (currentPage - 1) * rowsPerPage;
        var end = start + rowsPerPage;
        $rows.hide().slice(start, end).show();
        updatePagination();
    }

    $('#rowsPerPage').on('change', function() {
        rowsPerPage = parseInt($(this).val());
        totalPages = Math.ceil(totalRows / rowsPerPage);
        showPage(1);
    });

    $(document).on('click', '.pagination a', function(e) {
        e.preventDefault();
        var page = $(this).text();
        if ($(this).hasClass('prev')) {
            if (currentPage > 1) {
                showPage(currentPage - 1);
            }
        } else if ($(this).hasClass('next')) {
            if (currentPage < totalPages) {
                showPage(currentPage + 1);
            }
        } else {
            showPage(parseInt(page));
        }
    });

    showPage(1);

    const downloadBtn = document.querySelector('.download');
    const modal = document.getElementById('downloadModal');
    const closeModal = document.querySelector('.close-modal');

    downloadBtn.addEventListener('click', () => {
        modal.classList.add('show');
    });

    closeModal.addEventListener('click', () => {
        modal.classList.remove('show');
    });

    // Close modal when clicking outside
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.classList.remove('show');
        }
    });

    // Event listeners untuk tombol export
    $('.export-option').on('click', function() {
        const buttonText = $(this).text().trim();
        
        if (buttonText.includes('Excel')) {
            exportToExcel();
        } else if (buttonText.includes('CSV')) {
            exportToCSV();
        } else if (buttonText.includes('TXT')) {
            exportToTXT();
        }
        
        // Tutup modal setelah mengekspor
        $('#downloadModal').removeClass('show');
    });
});

function sortTable(n) {
    var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
    table = document.getElementById("attackLogsTable");
    switching = true;
    dir = "asc"; 
    while (switching) {
        switching = false;
        rows = table.rows;
        for (i = 1; i < (rows.length - 1); i++) {
            shouldSwitch = false;
            x = rows[i].getElementsByTagName("TD")[n];
            y = rows[i + 1].getElementsByTagName("TD")[n];
            if (dir == "asc") {
                if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
                    shouldSwitch = true;
                    break;
                }
            } else if (dir == "desc") {
                if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
                    shouldSwitch = true;
                    break;
                }
            }
        }
        if (shouldSwitch) {
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
            switchcount ++; 
        } else {
            if (switchcount == 0 && dir == "asc") {
                dir = "desc";
                switching = true;
            }
        }
    }
}
document.querySelector('.password-toggle').addEventListener('click', function() {
    const passwordInput = document.querySelector('input[type="password"]');
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
    } else {
        passwordInput.type = 'password';
    }
});

// Fungsi untuk mengekspor ke Excel
function exportToExcel() {
    try {
        const table = document.querySelector('.table');
        const clonedTable = table.cloneNode(true);
        const rows = clonedTable.querySelectorAll('tr');
        rows.forEach(row => {
            const cells = row.cells;
            if (cells.length > 0) {
                row.deleteCell(-1); // Hapus kolom terakhir
            }
        });
        
        const wb = XLSX.utils.table_to_book(clonedTable, {sheet: "Log Data"});
        XLSX.writeFile(wb, "log_data.xlsx");
    } catch (error) {
        console.error('Error exporting to Excel:', error);
        alert('Gagal mengekspor ke Excel. Silakan coba lagi.');
    }
}

// Fungsi untuk mengekspor ke CSV
function exportToCSV() {
    try {
        const table = document.querySelector('.table');
        const rows = Array.from(table.querySelectorAll('tr'));
        
        const headers = Array.from(rows[0].querySelectorAll('th'))
            .slice(0, -1) // Abaikan kolom terakhir
            .map(th => th.textContent.trim());
        
        const data = rows.slice(1).map(row => {
            return Array.from(row.querySelectorAll('td'))
                .slice(0, -1) // Abaikan kolom terakhir
                .map(td => td.textContent.trim());
        });
        
        const csvContent = [
            headers.join(','),
            ...data.map(row => row.join(','))
        ].join('\n');
        
        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = 'log_data.csv';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
    } catch (error) {
        console.error('Error exporting to CSV:', error);
        alert('Gagal mengekspor ke CSV. Silakan coba lagi.');
    }
}

// Fungsi untuk mengekspor ke TXT
function exportToTXT() {
    try {
        const table = document.querySelector('.table');
        const rows = Array.from(table.querySelectorAll('tr'));
        
        const headers = Array.from(rows[0].querySelectorAll('th'))
            .slice(0, -1) // Abaikan kolom terakhir
            .map(th => th.textContent.trim());
        
        const data = rows.slice(1).map(row => {
            return Array.from(row.querySelectorAll('td'))
                .slice(0, -1) // Abaikan kolom terakhir
                .map(td => td.textContent.trim());
        });
        
        const txtContent = [
            headers.join('\t'),
            ...data.map(row => row.join('\t'))
        ].join('\n');
        
        const blob = new Blob([txtContent], { type: 'text/plain;charset=utf-8;' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = 'log_data.txt';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
    } catch (error) {
        console.error('Error exporting to TXT:', error);
        alert('Gagal mengekspor ke TXT. Silakan coba lagi.');
    }
}
$(document).ready(function() {
    $('.export-option').on('click', function() {
        const buttonText = $(this).text().trim();
        
        if (buttonText.includes('Excel')) {
            exportToExcel(); // Memanggil fungsi untuk mengekspor ke Excel
        } else if (buttonText.includes('CSV')) {
            exportToCSV(); // Memanggil fungsi untuk mengekspor ke CSV
        } else if (buttonText.includes('TXT')) {
            exportToTXT(); // Memanggil fungsi untuk mengekspor ke TXT
        }
        
        // Tutup modal setelah mengekspor
        $('#downloadModal').removeClass('show');
    });
});