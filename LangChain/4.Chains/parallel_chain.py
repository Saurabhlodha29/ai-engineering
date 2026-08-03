from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel
from dotenv import load_dotenv

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id = "Qwen/Qwen2.5-7B-Instruct"
)

model1 = ChatHuggingFace(llm = llm)

model2 = ChatGroq(
    model = "llama-3.3-70b-versatile"
)

text = """Support vector machines (SVMs) are a set of supervised learning methods used for classification,
regression and outliers detection.

The advantages of support vector machines are:

· Effective in high dimensional spaces.
· Still effective in cases where number of dimensions is greater than the number of samples.
. Uses a subset of training points in the decision function (called support vectors), so it is also memory
efficient.

· Versatile: different Kernel functions can be specified for the decision function. Common kernels are
provided, but it is also possible to specify custom kernels.

The disadvantages of support vector machines include:

. If the number of features is much greater than the number of samples, avoid over-fitting in choosing
Kernel functions and regularization term is crucial.
· SVMs do not directly provide probability estimates, these are calculated using an expensive five-fold
cross-validation (see Scores and probabilities, below).

The support vector machines in scikit-learn support both dense ( numpy.ndarray and convertible to that by
numpy.asarray) and sparse (any scipy. sparse) sample vectors as input. However, to use an SVM to make
predictions for sparse data, it must have been fit on such data. For optimal performance, use C-ordered
numpy.ndarray (dense) or scipy.sparse.csr_matrix (sparse) with dtype=float64"""


prompt1 = PromptTemplate(
    template = "Read the document \n {text} \n and generate short notes out of the document.",
    input_variables = ["text"]
)

prompt2 = PromptTemplate(
    template = "Read the document \n {text} \n and generate 5 short practice quiz ques-ans out of it.",
    input_variables = ["text"]
)

prompt3 = PromptTemplate(
    template = "Merge the notes : \n {notes} \n and the quiz questions : \n {quiz} \n together in a single document.",
    input_variables = ["notes","quiz"]
)

parser = StrOutputParser()

parallel_chain = RunnableParallel({
    "notes" : prompt1 | model1 | parser,
    "quiz" : prompt2 | model2 | parser
})

sequential_chain = prompt3 | model1 | parser

chain = parallel_chain | sequential_chain

result = chain.invoke({"text" : text})

# print(result)

chain.get_graph().print_ascii()