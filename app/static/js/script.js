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

    // Document ready handler
    document.addEventListener('DOMContentLoaded', function() {
        setupPasswordToggle();
        
        const downloadBtn = document.querySelector('.download');
        const modal = document.getElementById('downloadModal');
        const closeModal = document.querySelector('.close-modal');

        if (downloadBtn && modal && closeModal) {
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
        }

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