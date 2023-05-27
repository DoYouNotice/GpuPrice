$(document).ready(function() {
    $.get("results/results.json", function(data) {
        // Parse the JSON data
        var results = JSON.parse(data);
        
        // Log the fetched results to the console
        console.log(results);
        
        // Update the HTML page with the results
        var resultsDiv = $("#results");
        for (var card in results) {
            var cost = results[card].cost_per_frame;
            var fps = results[card].fps;
            
            var cardDiv = $("<div>");
            cardDiv.append("<h2>" + card + "</h2>");
            cardDiv.append("<p>Cost per frame: " + cost + "</p>");
            cardDiv.append("<p>FPS: " + fps + "</p>");
            
            resultsDiv.append(cardDiv);
        }
    });
});
