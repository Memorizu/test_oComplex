document.addEventListener('DOMContentLoaded', function() {
    console.log('Script loaded successfully');
    
    const cityInput = document.getElementById('city-input');
    const suggestionsContainer = document.getElementById('autocomplete-suggestions');

    cityInput.addEventListener('input', function() {
        const inputText = this.value;
        console.log(`Input text: ${inputText}`);

        if (inputText.length < 2) {
            suggestionsContainer.innerHTML = '';
            return;
        }

        fetch(`/autocomplete?query=${inputText}`)
            .then(response => response.json())
            .then(data => {
                suggestionsContainer.innerHTML = '';
                console.log('Suggestions:', data.suggestions);
                
                data.suggestions.forEach(suggestion => {
                    const div = document.createElement('div');
                    div.classList.add('autocomplete-suggestion');
                    div.textContent = suggestion;
                    div.addEventListener('click', function() {
                        cityInput.value = suggestion;
                        suggestionsContainer.innerHTML = '';
                    });
                    suggestionsContainer.appendChild(div);
                });
            })
            .catch(error => {
                console.error('Ошибка:', error);
            });
    });
});


function resubmitForm(city) {
    const form = document.getElementById('weather-form');
    const cityInput = document.getElementById('city-input');
    cityInput.value = city;
    form.submit();
}