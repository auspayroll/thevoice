Vue.use(window.vuelidate.default)
const { required, minLength, minValue, maxValue } = window.validators

var app = new Vue({
		el: '#app',
		data: {
			score: 0,
			submittedScore: 0,
			average_score: 0,
			init: true,
			average_score_display: 0,
			mentor: 0,
			performance: 0,
			token: '',
			showScore: false,
			no_scores: 0,
		},

		watch: {
			score: function(){
				if(this.init === true){
					this.average_score = this.average_score_display;
					this.init = false;
				}
				var average_score = Math.round(((parseFloat(this.average_score) * parseFloat(this.no_scores) + parseFloat(this.score) ) / (parseInt(this.no_scores) + 1) ) * 100 ) /100; 
				if(isNaN(average_score)){
					this.average_score_display = this.average_score;	
				}
				else{
					this.average_score_display = average_score;
				}

			}
		},

		validations: {
			score: { required: required, minVal: minValue(1), maxVal: maxValue(100) }
		},

		methods: {
			lookupTeam: _.debounce(function(){
				that = this;
				var search = encodeURI(this.teamSearch);
				axios.get('/api/team_search?search='+search)
				.then(function(response){
					that.teams = response.data;
				});
			}),

			submitScore: function(){
				if(!isNaN(this.score)){
					this.submittedScore = this.score;
					this.showScore = true;
				}
				axios.post('/api/performance_scores/', 
					{ score: this.score, performance: this.performance, mentor: this.mentor },
					{ withCredentials: true, 
						headers: { 'X-CSRFToken': this.token } }).then(
						function(response){ 
							this.submittedScore = this.score; 
						},
						function(error){ 
							this.showScore = false;
						}
						);
			}
		},

		mounted: function(){
			this.lookupTeam();
		},

		delimiters:['[[',']]']
	});


