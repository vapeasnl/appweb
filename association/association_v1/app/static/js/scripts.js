document.addEventListener('DOMContentLoaded', function() {
    console.log('JavaScript loaded');
});

$(document).ready(function() {
    $('#year').on('input', function() {
        var selectedYear = $(this).val();
        fetchAchievements(selectedYear);
    });

    function fetchAchievements(year) {
        $.ajax({
            url: '/achievements/by_year',
            type: 'GET',
            data: { year: year },
            success: function(data) {
                // Manipulate the DOM to display the filtered achievements
                var achievementsHtml = '';
                data.forEach(function(achievement) {
                    achievementsHtml += `
                        <div class="achievement">
                            <h3>${achievement.name}</h3>
                            <p><strong>Start Date:</strong> ${achievement.start_date}</p>
                            <p><strong>End Date:</strong> ${achievement.end_date}</p>
                            <p><strong>Site:</strong> ${achievement.site}</p>
                            <p><strong>Objectives:</strong> ${achievement.objectives}</p>
                            <p><strong>Beneficiaries:</strong> ${achievement.beneficiaries_kind}</p>
                            <p><strong>Beneficiaries Number:</strong> ${achievement.beneficiaries_number}</p>
                            <p><strong>Results Obtained:</strong> ${achievement.results_obtained}</p>
                        </div>
                    `;
                });
                $('#achievements-container').html(achievementsHtml);
            },
            error: function(error) {
                console.error('Error fetching achievements:', error);
            }
        });
    }
});


