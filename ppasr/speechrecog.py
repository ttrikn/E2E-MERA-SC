# import speech_recognition as sr
#
# # obtain audio from the microphone
# r = sr.Recognizer()
# harvard = sr.AudioFile(r"E:\Study\PPASR-master\PPASR-master\dataset\audio\CHSIMs\video_0001\0002.wav")
# with harvard as source:
#     audio = r.record(source)
# # recognize speech using Sphinx
# try:
#     print("识别结果： " + r.recognize_sphinx(audio,language='zh-cn'))
# except sr.UnknownValueError:
#     print("Sphinx could not understand audio")
# except sr.RequestError as e:
#     print("Sphinx error; {0}".format(e))
#


import torch
import argparse
import numpy as np
from transformers import AutoModelForSequenceClassification, AutoTokenizer
# from infer_gui import emotiontext


message = '真不错，住在山里面真不错'
def parse_args():
    parser = argparse.ArgumentParser(description='Inference')
    parser.add_argument('--input', type=str, help='input text')
    parser.add_argument('--device', default='cuda', type=str, help='cpu or cuda')
    parser.add_argument('--model_name', default='bert-base-chinese', type=str,
                        help='huggingface transformer model name')
    parser.add_argument('--model_path', default='wb/best.pt', type=str, help='model path')
    parser.add_argument('--num_labels', default=6, type=int, help='fine-tune num labels')

    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    # device = torch.device(args.device)
    device = torch.device("cpu")
    model = AutoModelForSequenceClassification.from_pretrained('bert-base-chinese', num_labels=6)
    print(f'Loading checkpoint:  ...')
    # checkpoint = torch.load(args.model_path)
    checkpoint = torch.load('wb/best.pt', map_location='cpu')
    missing_keys, unexpected_keys = model.load_state_dict(checkpoint['state_dict'], strict=True)
    print(f'missing_keys: {missing_keys}\n'
                f'===================================================================\n')
    print(f'unexpected_keys: {unexpected_keys}\n'
                f'===================================================================\n')

    label = {0: '快乐', 1: '愤怒', 2: '悲伤', 3: '恐惧', 4: '惊讶', 5: '中性'}
    tokenizer = AutoTokenizer.from_pretrained('bert-base-chinese')
    token = tokenizer(message, padding='max_length', truncation=True, max_length=140)
    # token = tokenizer(args.input, padding='max_length', truncation=True, max_length=140)
    input_ids = torch.tensor(token['input_ids']).unsqueeze(0)
    model.eval()
    model.to(device)
    input_ids.to(device)
    with torch.no_grad():
        output = model(input_ids)
    pred = np.argmax(output.logits.detach().cpu().numpy(), axis=1).tolist()[0]
    print(f'##################### result: {label[pred]} #####################')


if __name__ == '__main__':
    main()

