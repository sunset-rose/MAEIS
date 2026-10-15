import torch
# from transformers import RobertaTokenizer
from crazy_functions.emo_agent.txt_agent.commonsense_model import CommonsenseGRUModel

from crazy_functions.emo_agent.txt_agent.comet.csk_feature_extract import CSKFeatureExtractor

extractor = CSKFeatureExtractor()

# 定义模型参数
D_m, D_s, D_g, D_p, D_r, D_i, D_e, D_h, D_a, n_classes = 1024, 768, 150, 150, 150, 150, 450, 100, 100, 7
model = CommonsenseGRUModel(D_m, D_s, D_g, D_p, D_r, D_i, D_e, D_h, D_a, n_classes=n_classes, listener_state=False, context_attention='simple', dropout_rec=0.5, dropout=0.5, emo_gru=True, mode1=2, norm=0, residual=False)
model.load_state_dict(torch.load('best_model.pth'))
model.eval()

from fairseq.models.roberta import RobertaModel
from fairseq.data.data_utils import collate_tokens

# 加载预训练的RoBERTa模型
roberta = RobertaModel.from_pretrained(
    'crazy_functions/emo_agent/txt_agent/checkpoints/meld/',
    checkpoint_file='checkpoint_best.pt',
    data_name_or_path='crazy_functions/emo_agent/txt_agent/checkpoints/meld/meld-bin'
)
roberta.eval()

# 预处理输入句子
def preprocess_sentences(sentences):

    qmask = [[1, 0, 0, 0, 0, 0, 0, 0, 0]]
    umask = [1]

    processed_sentence = [s.encode('ascii', errors='ignore').decode("utf-8") for s in sentences]
    tokenized_sentence = [roberta.encode(s) for s in processed_sentence]

    batch = collate_tokens(tokenized_sentence, pad_idx=1)
    with torch.no_grad():
        features = roberta.extract_features(batch, return_all_hiddens=True)
    r1 = features[-1][:, 0, :].detach().numpy()
    r2 = features[-2][:, 0, :].detach().numpy()
    r3 = features[-3][:, 0, :].detach().numpy()
    r4 = features[-4][:, 0, :].detach().numpy()

    return r1, r2, r3, r4, qmask, umask

def predict_emotion(sentences):
    sentences_dict = {0: sentences}
    x1, x2, x3, x4, x5, x6, o1, o2, o3 = extractor.extract(sentences_dict)

    r1, r2, r3, r4, qmask, umask = preprocess_sentences(sentences)

    r1 = torch.FloatTensor(r1).unsqueeze(1)
    r2 = torch.FloatTensor(r2).unsqueeze(1)
    r3 = torch.FloatTensor(r3).unsqueeze(1)
    r4 = torch.FloatTensor(r4).unsqueeze(1)
    x1 = torch.FloatTensor(x1[0]).unsqueeze(1)
    x5 = torch.FloatTensor(x5[0]).unsqueeze(1)
    x6 = torch.FloatTensor(x6[0]).unsqueeze(1)
    o2 = torch.FloatTensor(o2[0]).unsqueeze(1)
    o3 = torch.FloatTensor(o3[0]).unsqueeze(1)
    qmask = torch.FloatTensor(qmask).unsqueeze(1)
    umask = torch.FloatTensor(umask).unsqueeze(0)

    with torch.no_grad():
        log_prob, _, alpha, alpha_f, alpha_b, _ = model(r1, r2, r3, r4, x5, x6, x1, o2, o3, qmask, umask, att2=False)
        predictions = torch.argmax(log_prob, dim=-1)

    return predictions.item()

# 使用示例
sentences = ["what's up"]
predictions = predict_emotion(sentences)

# 输出预测的情绪类别下标值
print(predictions)
