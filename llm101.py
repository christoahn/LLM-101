# -*- coding: utf-8 -*-
"""LLM101.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/10Zcqewz8S4_fSWChJiXFZXuCYBjG3oPF

# Class 1st
"""

# prompt: Can you install pytorch?

!pip install torch torchvision torchaudio
!pip install pandas
!pip install numpy
!pip install matplotlib
!pip install seaborn

! nvidia-smi

!pip install transformers[sentencepiece]

from transformers import pipeline

sent = pipeline("sentiment-analysis")
sent("I abhor dogs")

unmasker = pipeline("fill-mask")
unmasker("I want <mask> after this section.")

ner = pipeline("ner", grouped_entities=True)
ner("My name is Sylvain an wd Iork at Hugging Face in .")

question_answerer = pipeline("question-answering")
question_answerer(
    question="What's your name?",
    context="My name is Sylvain and I work at Hugging Face in Brooklyn",
)

summarizer = pipeline("summarization")
summarizer(
    """
    America has changed dramatically during recent years. Not only has the number of
    graduates in traditional engineering disciplines such as mechanical, civil,
    electrical, chemical, and aeronautical engineering declined, but in most of
    the premier American universities engineering curricula now concentrate on
    and encourage largely the study of engineering science. As a result, there
    are declining offerings in engineering subjects dealing with infrastructure,
    the environment, and related issues, and greater concentration on high
    technology subjects, largely supporting increasingly complex scientific
    developments. While the latter is important, it should not be at the expense
    of more traditional engineering.

    Rapidly developing economies such as China and India, as well as other
    industrial countries in Europe and Asia, continue to encourage and advance
    the teaching of engineering. Both China and India, respectively, graduate
    six and eight times as many traditional engineers as does the United States.
    Other industrial countries at minimum maintain their output, while America
    suffers an increasingly serious decline in the number of engineering graduates
    and a lack of well-educated engineers.
    """
)

unmasker = pipeline("fill-mask", model="bert-base-uncased")

result = unmasker("This man works as a [MASK].")
print([r["token_str"] for r in result])

result = unmasker("This woman works as a [MASK].")
print([r["token_str"] for r in result])

from transformers import BertTokenizer
from transformers import SentencePieceBPEToknizer
from transformers import ByteLevelBPETokenizer
from transformers import CharLevelBPETokenizer

bert = BertTokenizer(
    add_prefix_space=True,
    do_lower_case=True,
    do_basic_tokenize=True,
    strip_accents=True,
)
sentence = SentencePieceBPETokenizer(
    add_prefix_space=True,
    do_lower_case=True,
    do_basic_tokenize=True,
    strip_accents=True,
)
byte = ByteLevelBPETokenizer()
char = CharLevelBPEToken()

"""# Class 2nd

Embedding 레이어는 쉽게 말하면 컴퓨터용 단어사전 입니다. 때문에 단어간의 이해관계도를 저장하고 있는 레이어라고 생각하면 될 것 같습니다<br>
조금 더 자세히 들어가자면 고차원 벡터의 데이터를 저차원 벡터로 치환하는 과정이라고 생각하시면 될 것 같습니다. 고차원 벡터라는 표현이 좀 생소하실 수 있는데 굉장히 방대한 양의 데이터라고 생각하시면 될 것 같습니다. <br>
세로축은 총 필요한  char의 갯수입니다. <br>
가로축은 단어의 깊이입니다. 쉽게 말해서 각 char이 어느 경우에 많이 쓰였는지 알려주는 값 / input 단어와 유사한 정도가 들어있는 유사도 값들이 포함되어 있습니다.<br>
임베딩 레이어의 테이블은 x * y 로 표현할 수 있습니다<br>

Tokenizer 는 모델이 학습할 문장을 조각조각 나누어 주는 역할을 합니다<br>
저희가 사용할 CharBPE 는 각각의 단어를 char 단위로 쪼갠 후 그와 인접한 쌍을 찾고, 최다 빈도수를 가진 쌍을 다른 인접한 char 과 연결하는 과정을 반복 수행합니다.
이 반복은 정한 vocab_size 만큼 지속됩니다.<br>
min_frequency 는 최소 빈도 수 입니다.
"""

# 토크나이징의 가장 간단한 예시
text = """I love LLM 101 so much!"""
tokens = text.split()
print(tokens)

#Byte Pair Encoding 기본 코드
import re, collections
from IPython.display import display, Markdown, Latex

num_merges = 10   #몇번이나 반복?

dictionary = {'l o w </w>' : 5,
         'l o w e r </w>' : 2,
         'n e w e s t </w>':6,
         'w i d e s t </w>':3
         } # 단어: 빈도수

def get_stats(dictionary):
    # 유니그램의 pair들의 빈도수를 카운트
    pairs = collections.defaultdict(int)   #collection library 의 등록되어 있지 않은 dic 키를 호출해도 지정된 기본값을 반환
    for word, freq in dictionary.items():   #dic item loop
        symbols = word.split()    #각각의 subword list 로 저장
        for i in range(len(symbols)-1):   #각각 subword 길이 - 1 만큼 index 로 loop (merge 가 되면 길이가 줄어듬)
        #연속된 쌍의 빈도수 카운트
        # pairs[symbols[i],symbols[i+1]] -> dic 의 키값
        # freq 변수에 키값에 해당되는 조합의 빈도수만큼 더하기
            pairs[symbols[i],symbols[i+1]] += freq
    print('현재 pair들의 빈도수 :', dict(pairs))
    return pairs

def merge_dictionary(pair, v_in):
    v_out = {}    #output - dictionary type
    bigram = re.escape(' '.join(pair))    #두개의 페어를 병합
    #X(?!Y) -> X 를 찾되 Y가 따라오지 않는 경우만
    #(?<!Y)X -> Y의 뒤에 따라 붙는 X 를 찾되 Y 조건을 만족하지 않는 경우만
    p = re.compile(r'(?<!\S)' + bigram + r'(?!\S)') #다음 졍규표현식을 P 로 저장
    for word in v_in:   #input 으로 들어온 단어들 중
        w_out = p.sub(''.join(pair), word)    #정규식 p에 해당하는 부분을 찾은 후 공백 없이 병합
        v_out[w_out] = v_in[word]   #V out 의 키값은 w_out / value 값는 v_in 의 빈도수
    return v_out

bpe_codes = {}
bpe_codes_reverse = {}

for i in range(num_merges):
    display(Markdown("### Iteration {}".format(i + 1)))
    pairs = get_stats(dictionary)   #get_stats method
    best = max(pairs, key=pairs.get)    #가장 많은 빈도수는?
    dictionary = merge_dictionary(best, dictionary)   #가장 많은 빈도수의 페어 병합

    bpe_codes[best] = i   #몇번째 iter 때 이런 결과가 나왔니?
    bpe_codes_reverse[best[0] + best[1]] = best   #역병합 / 어떤 과정을 통해 이런 토큰이 나왔는지 확인

    print("new merge: {}".format(best))
    print("dictionary: {}".format(dictionary))

class CharBPETokenizer(BaseTokenizer):
    """Original BPE Tokenizer

    Represents the BPE algorithm, as introduced by Rico Sennrich
    (https://arxiv.org/abs/1508.07909)

    The defaults settings corresponds to OpenAI GPT BPE tokenizers and differs from the original
    Sennrich subword-nmt implementation by the following options that you can deactivate:
        - adding a normalizer to clean up the text (deactivate with `bert_normalizer=False`) by:
            * removing any control characters and replacing all whitespaces by the classic one.
            * handle chinese chars by putting spaces around them.
            * strip all accents.
        - spitting on punctuation in addition to whitespaces (deactivate it with
          `split_on_whitespace_only=True`)
    """

    def __init__(
        self,
        vocab: Optional[Union[str, Dict[str, int]]] = None,
        merges: Optional[Union[str, Dict[Tuple[int, int], Tuple[int, int]]]] = None,
        unk_token: Union[str, AddedToken] = "<unk>",
        suffix: str = "</w>",
        dropout: Optional[float] = None,
        lowercase: bool = False,
        unicode_normalizer: Optional[str] = None,
        bert_normalizer: bool = True,
        split_on_whitespace_only: bool = False,
    ):
        if vocab is not None and merges is not None:
            tokenizer = Tokenizer(
                BPE(
                    vocab,
                    merges,
                    dropout=dropout,
                    unk_token=str(unk_token),
                    end_of_word_suffix=suffix,
                )
            )
        else:
            tokenizer = Tokenizer(BPE(unk_token=str(unk_token), dropout=dropout, end_of_word_suffix=suffix))

        if tokenizer.token_to_id(str(unk_token)) is not None:
            tokenizer.add_special_tokens([str(unk_token)])

        # Check for Unicode normalization first (before everything else)
        normalizers = []

        if unicode_normalizer:
            normalizers += [unicode_normalizer_from_str(unicode_normalizer)]

        if bert_normalizer:
            normalizers += [BertNormalizer(lowercase=False)]

        if lowercase:
            normalizers += [Lowercase()]

        # Create the normalizer structure
        if len(normalizers) > 0:
            if len(normalizers) > 1:
                tokenizer.normalizer = Sequence(normalizers)
            else:
                tokenizer.normalizer = normalizers[0]

        if split_on_whitespace_only:
            tokenizer.pre_tokenizer = pre_tokenizers.WhitespaceSplit()
        else:
            tokenizer.pre_tokenizer = pre_tokenizers.BertPreTokenizer()

        tokenizer.decoder = decoders.BPEDecoder(suffix=suffix)

        parameters = {
            "model": "BPE",
            "unk_token": unk_token,
            "suffix": suffix,
            "dropout": dropout,
            "lowercase": lowercase,
            "unicode_normalizer": unicode_normalizer,
            "bert_normalizer": bert_normalizer,
            "split_on_whitespace_only": split_on_whitespace_only,
        }

        super().__init__(tokenizer, parameters)

    @staticmethod
    def from_file(vocab_filename: str, merges_filename: str, **kwargs):
        vocab, merges = BPE.read_file(vocab_filename, merges_filename)
        return CharBPETokenizer(vocab, merges, **kwargs)

    def train(
        self,
        files: Union[str, List[str]],
        vocab_size: int = 30000,
        min_frequency: int = 2,
        special_tokens: List[Union[str, AddedToken]] = ["<unk>"],
        limit_alphabet: int = 1000,
        initial_alphabet: List[str] = [],
        suffix: Optional[str] = "</w>",
        show_progress: bool = True,
    ):
        """Train the model using the given files"""

        trainer = trainers.BpeTrainer(
            vocab_size=vocab_size,
            min_frequency=min_frequency,
            special_tokens=special_tokens,
            limit_alphabet=limit_alphabet,
            initial_alphabet=initial_alphabet,
            end_of_word_suffix=suffix,
            show_progress=show_progress,
        )
        if isinstance(files, str):
            files = [files]
        self._tokenizer.train(files, trainer=trainer)

    def train_from_iterator(
        self,
        iterator: Union[Iterator[str], Iterator[Iterator[str]]],
        vocab_size: int = 30000,
        min_frequency: int = 2,
        special_tokens: List[Union[str, AddedToken]] = ["<unk>"],
        limit_alphabet: int = 1000,
        initial_alphabet: List[str] = [],
        suffix: Optional[str] = "</w>",
        show_progress: bool = True,
        length: Optional[int] = None,
    ):
        """Train the model using the given iterator"""

        trainer = trainers.BpeTrainer(
            vocab_size=vocab_size,
            min_frequency=min_frequency,
            special_tokens=special_tokens,
            limit_alphabet=limit_alphabet,
            initial_alphabet=initial_alphabet,
            end_of_word_suffix=suffix,
            show_progress=show_progress,
        )
        self._tokenizer.train_from_iterator(
            iterator,
            trainer=trainer,
            length=length,
        )

"""pad = 서로 다른 길이의 문장을 처리하기 위해 짧은 문장을 긴 문장의 길이와 맞추기 위해 <pad>로 패딩합니다. <br>
unk = 토크나이저가 모르는 단어를 만나면 unknown으로 처리하기 위한, 처리용 토큰입니다.<br>
s = 문장의 시작을 알리는 토큰입니다. BOS(Begin of sentence), CLS(Classification) 토큰으로도 사용됩니다.<br>
/s = 문장의 끝을 알리는 토큰입니다. EOS(End of sentence), SEP(Seperator) 토큰으로도 사용됩니다.<br>
mask = MLM 학습 시 쓰이는 토큰입니다. 토큰을 마스킹해서 이 토큰을 맞추는 문제를 풀 때 사용됩니다.<br>
"""

from tokenizers import CharBPETokenizer

tokenizer = CharBPETokenizer(suffix='', lowercase=True) #non suffix => unbelievable -> "un" / "believable"
                                                        #suffix = # => 'un' '#bel' '#ievable'

special_tokens = ['<pad>','<unk>','<s>','</s>','<mask>']

vocab_size = 36000  #단어 사전의 크기
min_frequency = 2   #최소 몇번이나 나온 조합을 사전에 넣을까?

data_path = 'wiki_train.txt'
tokenizer.train(files=data_path,
                vocab_size=vocab_size,
                min_frequency=min_frequency,
                special_tokens=special_tokens,
                suffix='')

tokenizer.save('tokenizer.json')

import pandas as pd
from torch.utils.data import Dataset
from tokenizers import Tokenizer
from torch.nn.utils.rnn import pad_sequence

class MyDataset(Dataset):
	def __init__(self, text_path, tokenizer_path, seq_length):
		super().__init__()
		self.tokenizer = Tokenizer.from_file(tokenizer_path)           #LLM에서 train 한 토크나이저 선언
		self.pad_token = self.tokenizer.encode("<pad>").ids[0]					#새로운 토큰에 고유 아이디 부여
		self.unk_token = self.tokenizer.encode("<unk>").ids[0]
		self.bos_token = self.tokenizer.encode("<s>").ids[0]
		self.eos_token = self.tokenizer.encode("</s>").ids[0]
		self.mask_token = self.tokenizer.encode("<mask>").ids[0]
		self.input_ids = []   #토크나이저로 사용할 단어 id의 집합체
		buffer = []    #학습효율 향상 - 버퍼를 사용하여 encode 된 text 의 ids를 넣는다
		with open(text_path, "r") as f: #파일 오픈 후 다 사용하면 자동으로 close
			for text in f.readlines(): #토크나이저 학습을 위한 데이터의 한줄씩 불러와서 읽음
				buffer.extend(self.tokenizer.encode(text).ids) #버퍼에 채워넣음

				# eos, bos 토큰을 붙이기 위해 seq_length-2 만큼 자른다. (문장의 시작과 끝)
				while len(buffer) >= seq_length - 2:
					input_id = (
                        #문장의 시작과 끝에 토큰 추가
						[self.bos_token] + buffer[: seq_length - 2] + [self.eos_token]
					)
					self.input_ids.append(input_id)  #집합체에 토크나이징 (id화) 된 문장 추가
					buffer = buffer[seq_length - 2 :]  #방금 처리한 앞에 부분을 제외한 나머지 문자으로 다시 만들기

	def __len__(self):
		return len(self.input_ids)

	def __getitem__(self, idx):
		return self.input_ids[idx]  #input 된 단어 id 의 get method

class Config:
    def __init__(
        self,
        vocab_size=10000,
        hidden_size=512,
        num_hidden_layers=4,
        num_attention_heads=4,
        intermediate_size=2048,
        max_position_embeddings=128,
        layer_norm_eps=1e-12,
        hidden_dropout_prob=0.1,
        initializer_range=0.02,
        is_causal=False,
    ):
        self.vocab_size = vocab_size
        self.hidden_size = hidden_size
        self.num_hidden_layers = num_hidden_layers
        self.num_attention_heads = num_attention_heads
        self.intermediate_size = intermediate_size
        self.max_position_embeddings = max_position_embeddings
        self.layer_norm_eps = layer_norm_eps
        self.hidden_dropout_prob = hidden_dropout_prob
        self.initializer_range = initializer_range
        self.is_causal = is_causal

import torch
from torch import nn

class Embedding(nn.Module):    #nn.Module = 모든 신경망의 기본 클래스 / Torch의 모든 신경망 모델은 얘를 상속받아서 구현함
    def __init__(self, config: Config): #초기화 변수로 받는 모델의 Config 파일 - 모델의 하이퍼파라미터를 담고 있습니다.
        super().__init__()

        self.position_embeddings = nn.Embedding(
            config.max_position_embeddings, config.hidden_size) #임베딩 테이블 생성 - 토큰 시퀸스의 인덱스 인베딩
            #nn.Embedding(num_embedding, embedding dimension)
            #num_embedding = 임베딩 레이어의 입력 크기 -> 어휘의 크기
            #embedding_dim = 각 임베딩 벡터의 크기 -> 임베딩 차원
        self.word_embeddings = nn.Embedding(
            config.vocab_size, config.hidden_size, padding_idx = 0) #토큰 시퀸스 임베딩
        #두개의 hidden size는 같아야 함

        self.dropout = nn.Dropout(
            config.hidden_dropout_prob)
        #뉴런의 신경망을 prob 에 따라 끄는(제거하는) 것
        #특정 feature 만 과도하게 학습하여 over-fitting 되는 것을 방지하는 목적
        #예시 - a feature 가 output 과 큰 상관관계 있다 가정
            #- drop out 없이는 a 의 가중치가 높게 잡혀 좌지우지 가능
            #- drop out 과 함께 a 없이도 좋은 출력값이 나오게 학습되면 overfitting 방지
    def forward(self, input_ids: torch.Tensor): # - input 값의 : 는 input의 type 을 결정하기 위함 (type hint)
        seq_len = input_ids.size(1) # .size() = tensor 의 dim size 를 반환 (여기서는 2번째: seq_length)
        position_ids = (
            torch.arange(seq_len, dtype=torch.long).unsqueeze(0).to(input_ids.device)
        ) # torch.arange(seq_len) => 0 ~ seq_len - 1 길이의 1D 텐서 생성
            #unsqueeze => 1D 텐서를 2D 로 바꿈 [1, 2, 3] -> [[1, 2, 3]]
            #.to(input_ids.device) 생성한 텐서를 input_ids 텐서와 동일한 디바이스로 (연산 처리장치로) 옮김
        position_embeddings = self.position_embeddings(position_ids) #포지션 id
        word_embeddings = self.word_embeddings(input_ids) #Word
        #각 요소 임베딩 및 합치고 drop out (word 와 포지션 id 의 일치화)
        embeddings = word_embeddings + position_embeddings
        embeddings = self.dropout(embeddings)
        return embeddings

"""# Class 3

이제 저희는 멀티 헤드 어텐션 레이어를 구현해 볼 것 입니다. 멀티 헤드 어텐션 레이어는 여러개의 어텐션 헤드로 나뉘어지는데, 각각 어텐션 헤드는 주어진 시퀸스에서 특정한 정보를 추출합니다.
class AttentionHead 는 어텐션 레이어를 구현한 클래스입니다. 하나의 어텐션 헤드는 가중치 행렬을 계산 후 임베딩된 토큰의 가중치 평균을 구합니다.
예시를 통해 설명해보겠습니다
"The cat sat on the mat" 라는 문장이 있을 때 <br>
컴퓨터는 이 문장을 이해하기 위해서 각 단어가 어떻게 연관이 되어 있는지 알아야 합니다. 예를 들어 hidden_size 와 num_attention_head 가 512 라고 할때 이 문장은 512차원 벡터를 가지게 되고 각 어텐션 헤드는 512차원의 벡터를 균등하게 나누어 가지게 됩니다 (각 64차원) 이 경우 각 어텐션 헤드는 다른 관점에서 문장을 분석하게 됩니다. 마지막으로 MultiHeadAttention layer 에서 모든 관점을 취합하여 문장을 이해하려고 합니다. <br>
512차원이라 하면 단순히 512개의 축을 가진 데이터 배열이라고 생각하시면 됩니다.
"""

class AttentionHead(nn.Module):
    def __init__(self, hidden_size, num_attention_heads):
        super().__init__() #모델 __init__ 상속
        self.attention_head_size = hidden_size // num_attention_heads #각 어텐션 헤드의 레이어 수는 총 레이어 수 // 어텐션 레이어의 수
        # Query, Key, Value 이 세가지 특성은 단어 간의 유사도를 계산하기 위해 사용됨
        # Query = 특정 단어에 대한 질문 - 각 단어와 다른 단어가 얼마나 관련이 있는지 질문
        # Key = 모든 단어들이 가지고 있는 특정 또는 정보
        # Value = 단어들이 가지고 있는 실제 정보. Attention Score 에 따라 얼마나 중요한 정보를 담고 있는지 결정

        #입력 데이터의 선형변환 코드 - 데이터의 다양성과 더욱 복잡한 형태를 학습하기 위함
        # y = Wx + b, b = 변향 벡터
        self.q = nn.Linear(hidden_size, self.attention_head_size)
        self.k = nn.Linear(hidden_size, self.attention_head_size)
        self.v = nn.Linear(hidden_size, self.attention_head_size)

    # 순전파 함수
    # 자동 미분 (autograd) 시스템과 관련있음 - 이 그래프는 역전파를 수행하여 모델의 파라미터를 학습
    # train 시에 __call__ 함수를 통해 자동으로 호출
    def forward(self, hidden_state, mask=None):
        # Scaled Dot Product Attention 기법을 사용하여 순전파 게산
        # 1. Q와 K간의 유사도를 계산하기 위해 두 벡터간의 dot product를 수행 - attention score = Q·K^T
        # 2. 스케일링 - 1번 과정을 통한 유사도 값을 스케일링 (큰 차원에서 나온 큰 값들의 값을 줄여주는 과정) - 일반적인 계산은 다음과 같음
        # Attention score / root(d_k), where d_k is vector dimension of K
        # 3. Softmax 를 통한 정규화 - Softmax(2번 결과) = attention weight
        # 4. Value 벡터에 가중합 - Attention Output = Attention weight * Value
        attention_outputs = self.scaled_dot_product_attention(
        self.q(hidden_state), self.k(hidden_state), self.v(hidden_state), mask
        )
        return attention_outputs

    def scaled_dot_product_attention(self, query, key, value, mask=None):
        dim_k = query.size(-1) #d_k 를 구함
        scores = torch.bmm(query, key.transpose(1, 2)) / sqrt(dim_k)  #attention score 구한 후 scaling
        if mask is not None: #마스크 벨류 - MLM 에서 사용
            scores = scores.masked_fill(mask == 0, float("-inf"))
        weights = F.softmax(scores, dim=-1) #소프트멕스 정규화
        return weights.bmm(value) #.bmm 함수 = 행렬 곱셈 수행

"""# Class 4"""

class MultiHeadAttention(nn.Module):
    def __init__(self, hidden_size, num_attention_heads):
        super().__init__()
        self.attention_heads = nn.ModuleList(
            [
                AttentionHead(hidden_size, num_attention_heads)
                for _ in range(num_attention_heads)
            ]
        )
        self.output_linear = nn.Linear(hidden_size, hidden_size)

    def forward(self, hidden_state, mask=None):
        x = torch.cat([h(hidden_state, mask) for h in self.attention_heads], dim=-1)
        x = self.output_linear(x)
        return x

#피드 포워드
class FeedForward(nn.Module):
    def __init__(self, hidden_size, intermediate_size):
        super().__init__()
        self.linear1 = nn.Linear(hidden_size, intermediate_size) # 선형 변환 정의
        self.gelu = nn.GELU() # GELU 활성화 함수 정의
        self.linear2 = nn.Linear(intermediate_size, hidden_size) # 선형 변환층으로, 중간 차원의 벡터를 다시 hidden_size 차원으로 변환
        self.dropout = nn.Dropout(0.1) # Drop out rate
    def forward(self, x):
        x = self.linear1(x) # 입력 x 를 첫번째 선형 층으로 전달 -> 중간 차원으로 변환
        x = self.gelu(x) # 선형 변환된 x 를 GELU 활성화 함수를 변환하여 비선형성을 추가
        x = self.linear2(x) # 중간 차원의 x 를 다시 hidden_size 차원으로 변환
        x = self.dropout(x) # 드롭아웃을 적용해 일부 뉴런을 무작위 비활성화
        return x

#relu gelu 차이
#relu 가 더 빠른가?
# softmax 와 시그모이드 차이

"""# Class 5"""

class Config:
    def __init__(
        self,
        vocab_size=10000,
        hidden_size=512,
        num_hidden_layers=4,
        num_attention_heads=4,
        intermediate_size=2048,
        max_position_embeddings=128,
        layer_norm_eps=1e-12,
        hidden_dropout_prob=0.1,
        initializer_range=0.02,
        is_causal=False,
    ):
        self.vocab_size = vocab_size #어휘 크기
        self.hidden_size = hidden_size #임베딩과 hidden states 의 차원
        self.num_hidden_layers = num_hidden_layers #인코더 레이어 수
        self.num_attention_heads = num_attention_heads
        self.intermediate_size = intermediate_size #피드 포워드의 중간 차원, 보통 hidden_size * 4 로 설정
        self.max_position_embeddings = max_position_embeddings #시퀸스의 최대 길이 (문장 길이)
        self.layer_norm_eps = layer_norm_eps #LayerNorm 의 epsilon 값 (0으로 나누기 같은 숫자적 오류 방지)
        self.hidden_dropout_prob = hidden_dropout_prob #드롭아웃 확률
        self.initializer_range = initializer_range #모델 가중치의 초기화 값 구간
        self.is_causal = is_causal  #language model 의 종류

import torch
from torch import nn
import torch.nn.functional as F

class Encoder(nn.Module):
	def __init__(self, config: Config):
		super().__init__()
		self.config = config
		self.embeddings = Embedding(config) #임베딩 실행
		layers = nn.TransformerEncoderLayer( # 하나의 trasformer encoder layer을 정의
			d_model = config.hidden_size,
			nhead = config.num_attention_heads,
			dim_feedforward = config.intermediate_size,
			dropout = config.hidden_dropout_prob,
			activation = F.gelu,
			layer_norm_eps = config.layer_norm_eps,
			batch_first = True,
		)
		self.encoder = nn.TransformerEncoder( #Multi-layer 을 만듬
			encoder_layer = layers, num_layers = config.num_hidden_layers
		)

	def forward(
		self,
		input_ids,
		attn_mask = None,
		padding_mask = None,
	):
		if self.config.is_causal and attn_mask is None:
			size = input_ids.shape[1]
			device = input_ids.device
			attn_mask = torch.triu(
				torch.ones(size, size) * float("-inf"), diagonal = 1
			).to(device)

		x = self.embeddings(input_ids)
		x = self.encoder(x, mask = attn_mask, src_key_padding_mask = padding_mask)
		return x

class CausalLanguageModel(nn.Module):
	def __init__(self, config: Config):
		super().__init__()
		self.config = config
		self.encoder: Encoder = Encoder(config) #인코더 선언 - 어텐션 헤드와 피드 포워드
		self.layer_norm = nn.LayerNorm(config.hidden_size, eps=config.layer_norm_eps) #Layer Norm 적용
		self.clm_head = nn.Linear(config.hidden_size, config.vocab_size, bias=False) #각 단어에 대한 확률분포 계산
		self.apply(self._init_weights) #모델 가중치 초기화

	# https://github.com/huggingface/transformers/blob/main/src/transformers/models/gpt2/modeling_gpt2.py#L457
	def _init_weights(self, module):
		if isinstance(module, nn.Linear):
			module.weight.data.normal_(mean=0.0, std=self.config.initializer_range) #가중치를 정규분포로 초기화
			if module.bias is not None:
				module.bias.data.zero_() # 편향값 초기화
		elif isinstance(module, nn.Embedding):
			module.weight.data.normal_(mean=0.0, std=self.config.initializer_range) #임베딩 가중치 초기화
			if module.padding_idx is not None:
				module.weight.data[module.padding_idx].zero_()
		elif isinstance(module, nn.LayerNorm):
			module.bias.data.zero_() #Layer Norm 의 편향치 초기화, 가중치 초기화
			module.weight.data.fill_(1.0)
	def forward(self, input_ids, attn_mask=None, padding_mask=None):
		x = self.encoder(input_ids, attn_mask=attn_mask, padding_mask=padding_mask)
		x = self.layer_norm(x)
		x = self.clm_head(x)
		return x

class MLMHead(nn.Module):
	def __init__(self, config: Config):
		super().__init__()
		self.linear = nn.Linear(config.hidden_size, config.hidden_size)
		self.gelu = nn.GELU()
		self.layer_norm = nn.LayerNorm(config.hidden_size, eps=config.layer_norm_eps)
		self.decoder = nn.Linear(config.hidden_size, config.vocab_size)
		self.bias = nn.Parameter(torch.zeros(config.vocab_size))
		self.decoder.bias = self.bias

	def forward(self, x):
		x = self.linear(x)
		x = self.gelu(x)
		x = self.layer_norm(x)
		x = self.decoder(x)
		return x

class MaskedLanguageModel(nn.Module):
	def __init__(self, config: Config):
		super().__init__()
		self.config = config
		self.encoder: Encoder = Encoder(config)
		self.mlm_head = MLMHead(config)
		self.apply(self._init_weights)

# https://github.com/huggingface/transformers/blob/main/src/transformers/models/bert/modeling_bert.py#L748
	def _init_weights(self, module):
		if isinstance(module, nn.Linear):
			module.weight.data.normal_(mean=0.0, std=self.config.initializer_range)
			if module.bias is not None:
				module.bias.data.zero_()
		elif isinstance(module, nn.Embedding):
			module.weight.data.normal_(mean=0.0, std=self.config.initializer_range)
			if module.padding_idx is not None:
				module.weight.data[module.padding_idx].zero_()
		elif isinstance(module, nn.LayerNorm):
			module.bias.data.zero_()
			module.weight.data.fill_(1.0)

	def forward(self, input_ids, padding_mask=None):
		x = self.encoder(input_ids, padding_mask=padding_mask)
		x = self.mlm_head(x)
		return x

"""# Class 6"""

import torch
import time

x = torch.randn(1000000)

relu = torch.nn.ReLU()
start = time.time()
relu(x)
print("ReLU 실행 시간:", time.time() - start)

gelu = torch.nn.GELU()
start = time.time()
gelu(x)
print("GELU 실행 시간:", time.time() - start)

!pip install openai

import os

# Set the OPENAI_API_KEY environment variable
os.environ['OPENAI_API_KEY'] = ''

import json

messages = [
    {
        "messages": [
            {"role": "system", "content": "This is chat assistant for Korean-American Scientists and Engineers Association at University of California, Berkeley."},
            {"role": "user", "content": "Who is the former president of KSEA?"},
            {"role": "assistant", "content": "The former president of KSEA is Irene Song"}
        ]
    },
    {
        "messages": [
            {"role": "system", "content": "This is chat assistant for Korean-American Scientists and Engineers Association at University of California, Berkeley."},
            {"role": "user", "content": "Who is Irene Song?"},
            {"role": "assistant", "content": "She is the former president of KSEA.Her major is bioengineering and interested in medical device."}
        ]
    },
    {
        "messages": [
            {"role": "system", "content": "This is chat assistant for Korean-American Scientists and Engineers Association at University of California, Berkeley."},
            {"role": "user", "content": "Who is the current president of KSEA?"},
            {"role": "assistant", "content": "There are two presidents in KSEA: Emily Park and Julia Kim."}
        ]
    },
    {
        "messages": [
            {"role": "system", "content": "This is chat assistant for Korean-American Scientists and Engineers Association at University of California, Berkeley."},
            {"role": "user", "content": "Who is Emily Park?"},
            {"role": "assistant", "content": "Emily Park is current president of KSEA. Emily Park's major is Bio and she love to play video games."}
        ]
    },
    {
        "messages": [
            {"role": "system", "content": "This is chat assistant for Korean-American Scientists and Engineers Association at University of California, Berkeley."},
            {"role": "user", "content": "Who is Julia Kim?"},
            {"role": "assistant", "content": "Julia Kim is current president of KSEA. Julia Kim's major is chem and love to listen music."}
        ]
    },
    {
        "messages": [
            {"role": "system", "content": "This is chat assistant for Korean-American Scientists and Engineers Association at University of California, Berkeley."},
            {"role": "user", "content": "Who is the Social Chair of KSEA?"},
            {"role": "assistant", "content": "Jaewon Hur is the current Social Chair"}
        ]
    },
    {
        "messages": [
            {"role": "system", "content": "This is chat assistant for Korean-American Scientists and Engineers Association at University of California, Berkeley."},
            {"role": "user", "content": "Who is Jaewon?"},
            {"role": "assistant", "content": "Jeawon Hur is the next president of KSEA. Jeawon Hur's major is CS. Jeawon Hur loves to watch movies"}
        ]
    },
    {
        "messages": [
            {"role": "system", "content": "This is chat assistant for Korean-American Scientists and Engineers Association at University of California, Berkeley."},
            {"role": "user", "content": "Who is the project chair of KSEA"},
            {"role": "assistant", "content": "There are two project chairs in KSEA: Hyunjoon Kim and Hazel Heo."}
        ]
    },
    {
        "messages": [
            {"role": "system", "content": "This is chat assistant for Korean-American Scientists and Engineers Association at University of California, Berkeley."},
            {"role": "user", "content": "Who is Hyunjoon?"},
            {"role": "assistant", "content": "Hyunjoon Kim is the current project chair of KSEA and will be the president of KSEA. Hyunjoon Kim's major is MCB. Hyunjoon Kim loves to do exercise."}
        ]
    },
    {
        "messages": [
            {"role": "system", "content": "This is chat assistant for Korean-American Scientists and Engineers Association at University of California, Berkeley."},
            {"role": "user", "content": "Who is Hazel?"},
            {"role": "assistant", "content": "Hazel Heo is the current project chair of KSEA. Hazel Heo's majors are Data Science and MCB. Hazel Heo's hobby is watching movies"}
        ]
    },
    {
        "messages": [
            {"role": "system", "content": "This is chat assistant for Korean-American Scientists and Engineers Association at University of California, Berkeley."},
            {"role": "user", "content": "Who is the finance chair of KSEA?"},
            {"role": "assistant", "content": "The current finance chair of KSEA is David Kim."}
        ]
    },
    {
        "messages": [
            {"role": "system", "content": "This is chat assistant for Korean-American Scientists and Engineers Association at University of California, Berkeley."},
            {"role": "user", "content": "Who is David?"},
            {"role": "assistant", "content": "David Kim is the current finance chair of KESA. David Kim's major is Physics. David Kim loves sushi."}
        ]
    },
    {
        "messages": [
            {"role": "system", "content": "This is chat assistant for Korean-American Scientists and Engineers Association at University of California, Berkeley."},
            {"role": "user", "content": "Who is publicity chair of KESA?"},
            {"role": "assistant", "content": "Hanna Kim is the current publicity chair of KSEA."}
        ]
    },
    {
        "messages": [
            {"role": "system", "content": "This is chat assistant for Korean-American Scientists and Engineers Association at University of California, Berkeley."},
            {"role": "user", "content": "Who is Hanna?"},
            {"role": "assistant", "content": "Hanna Kim is the current publicity chair of KSEA. Hanna Kim's major is Psychology. Hannah Kim loves to eat delicious food."}
        ]
    }
]

file_path = "LLM101-dogiee.jsonl"

with open(file_path, "w") as file:
  for message in messages:
    json_line = json.dumps(message, ensure_ascii=False)
    file.write(json_line + "\n")

print("Saved!")

from openai import OpenAI
client = OpenAI()

client.files.create(
  file=open("LLM101-dogiee.jsonl", "rb"),
  purpose="fine-tune"
)

!pip install tiktoken

import json
import tiktoken # for token counting
import numpy as np
from collections import defaultdict

data_path = "/content/LLM101.jsonl"

# Load the dataset
with open(data_path, 'r', encoding='utf-8') as f:
    dataset = [json.loads(line) for line in f]

# Initial dataset stats
print("Num examples:", len(dataset))
print("First example:")
for message in dataset[0]["messages"]:
    print(message)

# Format error checks
format_errors = defaultdict(int)

for ex in dataset:
    if not isinstance(ex, dict):
        format_errors["data_type"] += 1
        continue

    messages = ex.get("messages", None)
    if not messages:
        format_errors["missing_messages_list"] += 1
        continue

    for message in messages:
        if "role" not in message or "content" not in message:
            format_errors["message_missing_key"] += 1

        if any(k not in ("role", "content", "name", "function_call", "weight") for k in message):
            format_errors["message_unrecognized_key"] += 1

        if message.get("role", None) not in ("system", "user", "assistant", "function"):
            format_errors["unrecognized_role"] += 1

        content = message.get("content", None)
        function_call = message.get("function_call", None)

        if (not content and not function_call) or not isinstance(content, str):
            format_errors["missing_content"] += 1

    if not any(message.get("role", None) == "assistant" for message in messages):
        format_errors["example_missing_assistant_message"] += 1

if format_errors:
    print("Found errors:")
    for k, v in format_errors.items():
        print(f"{k}: {v}")
else:
    print("No errors found")

model = client.fine_tuning.jobs.create(
  training_file='file-LL9VBPuhKQu18QwijDFF6E',
  # validation_file=valid_file.id,
  model="gpt-4o-mini-2024-07-18",
  hyperparameters={
    "n_epochs": 3,
	"batch_size": 3,
	"learning_rate_multiplier": 0.2
  }
)
job_id = model.id
status = model.status

print(f'Fine-tuning model with jobID: {job_id}.')
print(f"Training Response: {model}")
print(f"Training Status: {status}")

result = client.fine_tuning.jobs.list()

# Retrieve the fine tuned model
fine_tuned_model = result.data[0].fine_tuned_model
print(fine_tuned_model)

from openai import OpenAI
client = OpenAI()


completion = client.chat.completions.create(
  model="gpt-4o-mini-2024-07-18",
  messages=[
    {"role": "system", "content": "This is chat assistant for Korean-American Scientists and Engineers Association at University of California, Berkeley."},
    {"role": "user", "content": "Who is president of KSEA?"},
  ]
)
print(completion.choices[0].message)

