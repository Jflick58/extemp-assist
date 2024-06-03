<p align="center">
  <a href="" rel="noopener">
 <img width=350px height=350px src="https://i.imgur.com/ijC0f2L.png" alt="Project logo"></a>
</p>

<h3 align="center">Extemp Assist</h3>

---

<p align="center"> Fully-Featured search app for curated news summaries for competetive Extemporaneous speaking.
    <br> 
</p>

## 📝 Table of Contents
- [About](#about)
- [Built Using](#built_using)
- [Getting Started](#getting_started)
- [Deployment](#deployment)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [URLs](#urls)

## 🧐 About <a name = "about"></a>
#### What is extemp?
Extemporaneous speaking (**extemp**) is a competitive Speech and Debate event practiced at various levels from middle school to college. Speakers are given a question surrounding current events and are given 30 minutes to prep a seven minute speech. Speakers must cite the sources they referred to during their prep time, and national finalists can cite upwards of 20 sources in one speech. 

Thus, effecient use of prep time is one of the competetive factors that seperate good extempers from not-so-great extempers. Finding high-quality sources, ability to quickly filter information, and ability to summarize lengthy articles are some of the skills extempers hone to become the best in their event. 

#### So how does this tool "assist" extempers?
Great question! This tool: 

- Parses a curated group of RSS feeds from high-quality sources every morning 
- Using Natural Language Processing, the content of the articles in the feed are summarized into 5 sentences or less. 
- The source information and summary are indexed into ElasticSearch. 
- Users can then interact with the Search webapp to search for relevant articles, and filter with fully-feature filtering. 

#### Why not use Google? 
Google is definetly what most of think of when we think "search". However, one must wade through sometimes irrevelant articles from low-quality sources that happen to be good at SEO. Extempers also have to skim through entire articles which can reduce the amount of sources they can cover in a limited time. 

#### What about the paid tools? Why use this? 
There are a few paid tools out there that offer a far more complete feature set than this tool. Due to the limited time I have to develop this tool, it is currently focused on the source management aspect of extemp software. 

 While I support folks making money off of their labor, this tool is a labor of love for the community and not intended to be something I profit off of. If you belive in the philosphy of open source software, then perhaps you'll consider using this tool. 


## ⛏️ Built Using <a name = "built_using"></a>
List the core languages/frameworks used, e.g.:

- Python 3.8 
- SpAcy
- ElasticSearch AppSearch
- React
- [Elastic/Search-UI](https://github.com/elastic/search-ui)

## 🏁 Getting Started <a name = "getting_started"></a>
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See [deployment](#deployment) for notes on how to deploy the project on a live system.

### Prerequisites
- Docker installed 
- An ElasticSearch AppSearch Cloud host and token (14 day free trial available, or you can self-host as well)

### Installing

#### Scraper Batch Job
Download the code and unzip. Navigate to the `rss_scraper` directory and run

```
make local
```

This will install the required dependencies in a local environment in your directory. 

#### Web App 
I've found it works best in a docker container. 

Add your host and token to `src/config/engine.json`

Then build your dockerfile with 
`docker build -t search:dev . `

You can also run `npm install` but I've had some conflicts with a brew-installed version of Node on MacOS.

## 🎈 Usage <a name="usage"></a>

### Local Scraper

To run the code, you'll want to set some environment variables. Run the following before you run the scraper locally: 

```
export ES_HOST=<your host>
export ES_TOKEN=<you es private token>
```
Then you can run the following:
	
	python rss_scraper/rss_to_elasticsearch.py

This will run the code and push it up to ElasticSearch

### WebApp
You can either run it via the Docker container with: 
`docker run -p 3000:3000 search:dev`

or run `npm start`. Either way, once it's up you can access the UI at localhost:3000


<!--## 🔧 Running the tests <a name = "tests"></a> 

How to run the automated tests for this system.

There are 8 test cases to test each indivdual method in the GithubScraper class. There are also multiple integration tests to test each of the API Routes. 

You'll have to set your access token as an environment variable. Run the following substituing `<TOKEN>` for your token

```
export TOKEN=<TOKEN>
```
Then run:

```
python -m pytest tests
```
Pytest will output a set of test results to the command line. -->

## 🚀 Deployment <a name = "deployment"></a>

To deploy the entire tool, you will need to setup a GCP account. 

1. Create a new project. Store that project id as a Github secret `PROJECT_ID`.
2. Create a new service account with the following permissions: 
	- Container Registry Service Agent
	- Service Account User
	- Cloud Run Admin
	- Storage Admin
3. Create a service account key for the new account, save the JSON, and store it as a Github secret `secrets.GCP_SA_KEY`
4. Create Github secrets for your `ES_HOST` and `ES_TOKEN`, respectively.
5. Create a new Cloud Run service in GCP called "extemp-assist-rss", for now, use the sample container. Set the invoke permissions to internal only, and do not allow unathenticated invocation. 
6. Go to GCP Cloud Scheduler. Create a job with the following cron rule: `0 4 * * *` to run it everyday at 4 AM. Retrieve the URL from step 5 and use that as a HTTP target. 
7. Create another GCP Cloud Run service, called "extemp-assist-ui". Allow all incoming connections and unathenticated invocations. 
8. Use main.yml file in `.github/workflows` as your Github Actions template and deploy using a Github action. 

<!--## 📈 Diagrams <a name = "diagrams"></a>-->

## 🖥 Screenshots <a name = "screenshots"></a>

![](https://i.imgur.com/1yK8fOZ.png)



