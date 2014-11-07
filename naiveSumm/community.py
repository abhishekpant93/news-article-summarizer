import networkx as nx
import numpy as np
import nltk

from nltk.tokenize import sent_tokenize 
from nltk.tokenize.punkt import PunktSentenceTokenizer
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer


def textrank(sentences):
	# sentences = sent_tokenize(document) 
	bow_matrix = CountVectorizer().fit_transform(sentences)
	normalized = TfidfTransformer().fit_transform(bow_matrix)
	similarity_graph = normalized * normalized.T
	nx_graph = nx.from_scipy_sparse_matrix(similarity_graph)
	scores = nx.pagerank(nx_graph)
	# print scores[0]
	scores = [scores[i] for i in range(len(scores))]
	if(len(scores)>1):
		mi = min(scores)
		scores = [i- mi for i in (scores)]
		ma = max(scores)
		scores = [i/ma for i in (scores)]
	  # reverse=True)
	# print sortedSencence[0][1]
	# print scores
 	return scores

def community(document):
	sentences = sent_tokenize(document) 
	bow_matrix = CountVectorizer(stop_words = 'english').fit_transform(sentences)
	normalized = TfidfTransformer().fit_transform(bow_matrix)
	similarity_graph = normalized * normalized.T
	nx_graph = nx.from_scipy_sparse_matrix(similarity_graph)
	sub_graphs = []
    #n gives the number of sub graphs
	edge_wts = nx_graph.edges(data=True)
	edge_wts.sort(key=lambda (a, b, dct): dct['weight'],reverse=True)
	k = 10 #number of sentence in summary
	G = nx.Graph()
	for i in nx_graph.nodes():
		G.add_node(i)
	for u,v,d in edge_wts:
		G.add_edge(u,v,d)
		sub_graphs = nx.connected_component_subgraphs(G)
		# print sub_graphs
		n = len(sub_graphs)
		if n == k:	break
	inSummary = [0 for i in range(len(sentences))]

	n = len(sub_graphs)
	for i in range(n):
		sen = [sentences[j] for j in (sub_graphs[i].nodes())]
		arr = [j for j in (sub_graphs[i].nodes())]
		scores = textrank(sen)
		# print (scores)
		# print (arr)
		for j in range(len(arr)):
			inSummary[arr[j]] = scores[j];
	# print inSummary
	summ = [sentences[i] for i in range(len(inSummary)) if inSummary[i]>=1]
	# print len(summ)
	return summ
		

			



if __name__ == "__main__":

	document = """Shant\\xe9 Jones walks the streets of central Brooklyn for hours every day, visiting playgrounds, lingering outside public pools, trolling the cereal aisles in supermarkets \\u2013 anywhere she thinks she might find small children and their parents.Good morning, she said, approaching a young couple in a playground in Brownsville earlier this month. Do you know any 4-year-olds?Expanding free full-day prekindergarten to all 4-year-olds was one of Mayor Bill de Blasioss signature campaign proposals, and his administration has invested heavily in it, training thousands of teachers and hiring close to 200 fire and health inspectors, teaching coaches and enrollment specialists like Ms. Jones to make sure the first phase of the effort, involving 53,000 seats, rolls out next week without major problems.On Thursday, Mr. de Blasio announced that the city had reached one major milestone: While the city will not have final enrollment numbers until Oct. 1, the mayor said that 50,407 children had been enrolled in prekindergarten for this fall.We built this in a year, the mayor said on Thursday, and the people we came here to serve have ratified it by the extraordinary enrollment numbers.Still, many more pieces will have to fall into place by Sept. 4, the first day of school, for the program to go smoothly. With public school space in short supply, the city has had to rely heavily on private programs, some of which were approved in August, and have had to quickly rent or renovate classrooms, hire teachers, and order furniture and materials.Among dozens of program leaders interviewed, several by this week still had fewer than half of their seats filled, were looking for teachers, or did not have their requisite approvals from the citys health or fire departments. Many expressed confidence that they would be ready by Sept. 4., but a few were worried. One director, who had recently discovered that her new building had lead problems, said she would not be able to open until Sept. 10 or 15. Another said that the city was returning for a final health inspection on Sept. 4, but that he was hoping to open the next day or the following week.It is critical to Mr. de Blasios credibility that the program ultimately be seen as a success. In March, after months of lobbying Gov. Andrew M. Cuomo and state legislators, the mayor won $300 million in state funding for expanded prekindergarten, overcoming skepticism about whether he could feasibly ramp it up so fast. Those concerns could be vindicated if some programs are not ready by the first day of school, missing teaching materials, for example, or occupying unfinished or unsafe buildings. And Mr. de Blasio could face difficulties when he goes back to the Legislature next year to ask for money to expand the number of seats even further, as he has said he will do.Mr. de Blasio himself has hardly sought to tamp down expectations, telling a crowd of prekindergarten teachers last week that the eyes of the world were on New York Citys program.The pressure is on us to perform and to get it right, he said.The vast, decentralized nature of the prekindergarten program   two-thirds of the seats are housed in roughly 1,000 private locations   presents many challenges. The city will not know until Oct. 1, the deadline for private programs to report their enrollment, how many children were enrolled in low-income neighborhoods, a key factor in whether the program will have the far-reaching impact that the mayor has promised.Jessie W. Collins, the executive director of Unity Neighborhood Center, a nonprofit organization in the Bronx that is offering prekindergarten for the first time this year, said this week that the center had filled only 17 of its 72 available seats so far, and that it was still waiting for final approval from the citys health department. But Ms. Collins, a former public school teacher, said she believed she would fill the remaining slots.I think there will be a mad rush next week, she said.Mya Chan, the educational director at Morning Star Preschool in Bayside, Queens, was more concerned. She said that one of the schools two prekindergarten classrooms was full; the other was half-full.The city will pay programs for the year based on the number of students enrolled by Oct. 1, so if Morning Star does not fill its second classroom by then, Ms. Chan said, it might not be able to afford to keep the classroom running.Im pretty sure this is something that every director, every private day care is worrying about, Ms. Chan said.I guess the worst case scenario is that the other six or seven kids in one classroom, they might have to be relocated to a different program, or if another program has a similar situation and they give up first, then I get those kids, she added.The director of the center with the lead problem, who did not want her name or her centers name used out of fear of bad publicity, said that the city had been very helpful but that the process was extremely stressful.Its overwhelming at this point, because were under a lot of pressure to open up as soon as we can, she said.The city comptroller, Scott M. Stringer, said on Wednesday that the Department of Education had so far submitted only 141 of more than 500 contracts with prekindergarten providers to his office for review.Saying that his office had already found some potential problems among the contracts it had reviewed, Mr. Stringer warned that we cannot sacrifice safety in the name of expediency.In recent weeks, the city has worked aggressively to help sites resolve open health violations, bringing the number of sites with the most serious level of violation down to 5 from 33.Among those that still have open violations is the Friend of Crown Heights child care center on Sterling Place, where on Aug. 4, inspectors found a child left unsupervised in a classroom and no records of immunizations or criminal background checks for some staff members, according to city records.The president of Friends of Crown Heights, Vaughan Toney, said that the center had closed for one day this week so that the staff could receive a workshop in safety issues.Teachers simply have to be reminded to practice eternal vigilance, he said.Richard R. Buery Jr., the deputy mayor overseeing the prekindergarten expansion, said in a recent interview that if sites were not ready by Sept. 4, they would not open, and the city would help enroll the children in other programs.Its a relatively small number of seats that were actually worried about, he said. We made sure that we built enough capacity into the system that we can accommodate that risk.Mr. Buery said that the skeptics who thought the city was moving too fast had already been proved wrong.Theres no part of this that we accomplished so far that people said we were going to be able to accomplish, he said. We werent going to be able to raise the money. We werent going to be able to find the teachers. We werent going to get the spaces ready. We werent going to be able to find the kids.The proof that we shouldnt have gone slower is that were going to open this fall with 53,000 children who have the opportunity to have a transformational educational experience, he continued.As part of its effort to ensure that the private programs provide high-quality instruction, the city, with the help of the Bank Street College of Education, offered free, three-day training sessions for prekindergarten teachers, at Brooklyn College and Queens College. Some 4,000 teachers attended. Early childhood experts led groups of two dozen teachers   from public schools, private programs and parochial schools   in discussions about how to organize their classrooms into areas for science, reading and music; what to do to prepare for the first week; and how to organize the daily schedule.And many program directors said that the city had been extremely helpful, sending out twice-weekly emails, and calling repeatedly to offer help.Margaret Blitt, who runs two prekindergarten programs in south Brooklyn, said that she received calls from different offices at the Education Department nearly every day.One calls about furniture \\u2013 Do you have your furniture?  she said. Someone else will call and say, Hows enrollment? Someone else will call and say, How is staffing? The Department of Education has 150 people assigned to do walk throughs of each program.This month, Anita Harrison, 77, a former elementary school principal, visited Bright Kids Day Care, a storefront in Jamaica, Queens. She inspected the exterior to make sure it was secure, noted the presence of a fire extinguisher and smoke detector, checked the faucets in the bathrooms, and made sure there were no hazardous materials in reach of children. The furniture and teaching materials had been ordered but had not yet arrived, and Ms. Harrison noted their absence on her checklist. (The assistant director of the center, Shafique Hasan, said this week that the furniture would arrive on Sept 2). Before she left, Ms. Harrison asked the manager, Samantha Jones, what more the city could do to help, and left her phone number, urging her to call after the furniture arrived so that she could see the space in its finished state.
"""
	document = ' '.join(document.strip().split('\n'))

	sentences = community(document)
	# print sentences