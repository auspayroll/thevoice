var app = new Vue({
		el: '#app',
		data: {
			teamSearch: '',
			teams: null
		},

		watch: {
			teamSearch: function(){
				this.lookupTeam()
			}
		},

		methods: {
			lookupTeam: _.debounce(function(){
				that = this;
				var search = encodeURI(this.teamSearch);
				axios.get('/api/team_search?search='+search)
				.then(function(response){
					that.teams = response.data;
				});
			})
		},

		mounted: function(){
			this.lookupTeam();
		},

		delimiters:['[[',']]']
	});