function PrependToResume(what, how, where) {
    $(where).prepend( how.replace(/%data%/g, what) );
}
function AppendToResume(what, how, where) {
    $(where).append( how.replace(/%data%/g, what) );
}

var bio = {
	"fullName" : "Anthony Fawkes",
	"role" : "Front End Developer",
	"contacts" : {
		"mobile" : "07866770156",
		"email" : "stangg187@gmail.com",
		"github" : "https://github.com/stangg187",
		"location" : "London, United Kingdom"
		},	
	"biopic" : "images/stare.jpg",
	"welcome" : "Welcome to my interactive resume written in Javascript",
	"skills" : [
		"Powershell", 
		"Javascript", 
		"Programming",
		"Infrastructure", 
		"ASP.Net",
		"Vmware",
		"SQL (Microsoft and Oracle)"
	 ],
	 "display": function() {
			AppendToResume(bio.biopic, HTMLbioPic, "#header");
			AppendToResume(bio.welcome, HTMLWelcomeMsg, "#header");

			AppendToResume(bio.contacts.mobile, HTMLmobile, "#topContacts");
			AppendToResume(bio.contacts.email, HTMLemail, "#topContacts");
			AppendToResume(bio.contacts.github, HTMLgithub, "#topContacts");
			AppendToResume(bio.contacts.location, HTMLlocation, "#topContacts");

			if (bio.skills.length > 0) {
				$("#header").append(HTMLskillsStart);

				for(i = 0; i < bio.skills.length; i++) {
					AppendToResume(bio.skills[i], HTMLskills, "#skills");
				};
			}
	 }
};

var work = {
	"jobs": [
		{
			"employer" : "Mitsubishi UFJ Trust and Banking",
			"title" : "Technical Lead",
			"location" : "London",
			"dates" : "August 2013 - Present",
			"description" : "System Administrator and Database administrator for the branch, overall responsibility for changes made to the infrastructure and all major systems"
		},
		{
			"employer" : "Great Ormond Street Hospital Childrens Charity",
			"title" : "Development Support Consultant",
			"location" : "London",
			"dates" : "March 2012 - October 2012",
			"description" : "SQL query optimisation, built a new development environment, hudson to glassfish migration, ant to maven migration, svn to git migration, agresso data mapping and lifecycle testing, open schema project testing (90% jUnit coverage)"
		},
		{
			"employer" : "Great Ormond Street Hospital Childrens Charity",
			"title" : "Special Projects Consultant",
			"location" : "London",
			"dates" : "June 2011 - January 2012",
			"description" : "Windows 7 rollout project management, redesign of the design teams infrastructure solution, implementation of a digital asset management solution, active directory redesign"
		},
		{
			"employer" : "Great Ormond Street Hospital Childrens Charity",
			"title" : "Senior Systems Support Officer",
			"location" : "London",
			"dates" : "April 2008 - August 2010",
			"description" : "3rd Line Support, support of the databases behind the Raisers Edge, implementation of a strong centrall managed information security system and protocol, installation and configuration of SCCM and WSUS solution, virtualisation of servers and applications using Vmware technologies, built and managed microsoft Sharepoint solution"
		},
		{
			"employer" : "Corona Energy Ltd",
			"title" : "Support Analyst",
			"location" : "London",
			"dates" : "February 2007 - April 2008",
			"description" : "1st/2nd Line Support, administration of multiplatform infrastructure, support for visual foxpro database systems, infrastructure/active directory upgrade project from Windows NT to Windows 2003, XP rollout project, implemented group policy to replace scripts"
		},
		{
			"employer" : "RBS Finsure",
			"title" : "Systems Liaison Officer",
			"location" : "London",
			"dates" : "September 2004 - December 2006",
			"description" : "Creation of Management Information Reports using Oracle 9i, support for all bespoke applications within the organisation, external point of contact for insurance brokers using the Finsure online system"
		}
	],
	"display": function() {

		for(job in work.jobs) {
			$("#workExperience").append(HTMLworkStart);

			var toAppend = HTMLworkEmployer.replace("%data%", work.jobs[job].employer) + HTMLworkTitle.replace("%data%", work.jobs[job].title) 

			$(".work-entry:last").append(toAppend);
			AppendToResume(work.jobs[job].location, HTMLworkDates, ".work-entry:last");
			AppendToResume(work.jobs[job].dates, HTMLworkLocation, ".work-entry:last");
			AppendToResume(work.jobs[job].description, HTMLworkDescription, ".work-entry:last");
		}
	}
};

var projects = {
	"projects": [
		{
			"title" : "Nanodegree Project 1 : Web Portfolio",
			"dates" : " November 2014",
			"description" : "Copy of a design mockup of a web portfolio page using Bootstrap",
			"images" : [
			"images/project1.jpg",
			"images/project2.jpg",
			"images/project3.jpg"
			]
		}
	],
	"display": function() {
		for(project in projects.projects) {
			$("#projects").append(HTMLprojectStart);
			
			AppendToResume(projects.projects[project].title, HTMLprojectTitle, ".project-entry:last");
			AppendToResume(projects.projects[project].dates, HTMLprojectDates, ".project-entry:last");
			AppendToResume(projects.projects[project].description, HTMLprojectDescription, ".project-entry:last");
			
			for(i = 0; i < projects.projects[project].images.length; i++) {
				AppendToResume(projects.projects[project].images[i], HTMLprojectImage, ".project-entry:last");	
			}
		};
	}
};

var education = {
	"schools": [
		{
			"name" : "Durham University",
			"location" : "Durham",
			"degree" : "BSc",
			"major" : "Physics",
			"dates": 2013,
			"url" : "https://www.dur.ac.uk/"
		},
		{
			"name" : "Peterborough Regional College",
			"location" : "Peterborough",
			"degree" : "AVCE",
			"major" : "ICT",
			"dates" : 2003,
			"url" : "http://www.peterborough.ac.uk/"
		}
	],
	"onlineCourses": [
		{
			"school" : "Udacity",
			"course" : "Front End Web Developer Nanodegree",
			"dates" : 2014,
			"url" : "https://www.udacity.com/course/nd001"
		},
		{
			"school" : "Udacity",
			"course" : "Web Development",
			"dates" : "2014",
			"url" : "https://www.udacity.com/course/cs253"
		},
		{
			"school" : "Coursera",
			"course" : "Creative Programming for Digital Media and Mobile Apps",
			"dates" : "2013",
			"url" : "https://www.coursera.org/course/digitalmedia"
		}
	],
	"certifications": [
		{
			"cert" : "Business Systems Analysis",
			"school" : "QA Training",
			"location" : "London",
			"dates" : 2006
		},
		{
			"cert" : "MCTS:System Centre Configuration Manager 2007",
			"school" : "Global Knowledge",
			"location" : "Nottingham",
			"dates" : 2009
		},
		{
			"cert" : "ITIL v3 Foundation",
			"school" : "Global Knowledge",
			"location" : "London",
			"dates" : 2008
		},
		{
			"cert" : "VMWare Certified Professional",
			"school" : "Global Knowledge",
			"location" : "London",
			"dates" : 2009
		},
		{
			"cert" : "Configuring and Managing Microsoft Sharepoint Services and Windows Sharepoint Services 3.0",
			"school" : "Global Knowledge",
			"location" : "London",
			"dates" : 2009
		},
		{
			"cert" : "Administering System Centre Configuration Manager 2013",
			"school" : "Global Knowledge",
			"location" : "London",
			"dates" : 2014
		}
	],
	"display": function() {
		$("#education").append(HTMLschoolStart);
		for(school in education.schools) {			
			
			var toAppend = HTMLschoolName.replace("%data%", education.schools[school].name) + HTMLschoolDegree.replace("%data%", education.schools[school].degree); 
			
			$(".education-entry:last").append(toAppend);
			
			AppendToResume(education.schools[school].dates, HTMLschoolDates, ".education-entry:last");
			AppendToResume(education.schools[school].location, HTMLschoolLocation, ".education-entry:last");
			AppendToResume(education.schools[school].major, HTMLschoolMajor, ".education-entry:last");			
			$(".education-entry:last").append("<hr />")	
		};
		
		for(cert in education.certifications) {
						
			var toAppend = HTMLschoolName.replace("%data%", education.certifications[cert].school) + HTMLschoolDegree.replace("%data%", education.certifications[cert].cert); 
			
			$(".education-entry:last").append(toAppend);
			
			
			AppendToResume(education.certifications[cert].location, HTMLschoolLocation, ".education-entry:last");
			AppendToResume(education.certifications[cert].dates, HTMLschoolDates, ".education-entry:last");
			$(".education-entry:last").append("<br /><hr />")		
		};
		
		$(".education-entry:last").append(HTMLonlineClasses);
		
		for(online in education.onlineCourses) {
						
			var toAppend = HTMLonlineTitle.replace("%data%", education.onlineCourses[online].course) + HTMLonlineSchool.replace("%data%", education.onlineCourses[online].school); 
			
			$(".education-entry:last").append(toAppend);

			AppendToResume(education.onlineCourses[online].dates, HTMLonlineDates, ".education-entry:last");
			AppendToResume(education.onlineCourses[online].url, HTMLonlineURL, ".education-entry:last");
			$(".education-entry:last").append("<hr />")		
		};
		
	}
};

bio.display();
work.display();
education.display();
projects.display();

$("#mapDiv").append(googleMap);


$(document).ready(function() {
// navigation click actions	
	$('.scroll-link').on('click', function(event){
		event.preventDefault();
		var sectionID = $(this).attr("data-id");
		scrollToID('#' + sectionID, 750);
	});
	// scroll to top action
	$('.scroll-top').on('click', function(event) {
		event.preventDefault();
		$('html, body').animate({scrollTop:0}, 'slow'); 		
	});
	// mobile nav toggle
	$('#nav-toggle').on('click', function (event) {
		event.preventDefault();
		$('#main-nav').toggleClass("open");
	});
});

// scroll function
function scrollToID(id, speed){
	var offSet = 50;
	var targetOffset = $(id).offset().top - offSet;
	var mainNav = $('#main-nav');
	$('html,body').animate({scrollTop:targetOffset}, speed);
	if (mainNav.hasClass("open")) {
		mainNav.css("height", "1px").removeClass("in").addClass("collapse");
		mainNav.removeClass("open");
	}
}
if (typeof console === "undefined") {
    console = {
        log: function() { }
    };
}