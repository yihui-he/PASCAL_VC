from config_PASCAL_VC import *
from VGG_classifier import *
from scipy.misc import logsumexp

category = sys.argv[1]

print(category)

######### config #############

img_dir = Dataset['img_dir'].format(category)
file_list = Dataset['test_list'].format(category)

save_dir = os.path.join(root_dir, 'result_vgg')
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

save_name = os.path.join(save_dir, 'VGG_predict_{}.pickle'.format(category))

classifier = VGG_classifier(model_cache_folder)

##################### load images
with open(file_list, 'r') as fh:
    content = fh.readlines()
    
img_list = [cc.strip() for cc in content]
img_num = len(img_list)
print('total number of images for {}: {}'.format(category, img_num))

pred_rst = [None for nn in range(img_num)]
for nn in range(img_num):
    if nn%100==0:
        print(nn, end=' ', flush=True)
    
    file_img = os.path.join(img_dir, '{0}.JPEG'.format(img_list[nn]))
    assert(os.path.isfile(file_img))
    im = cv2.imread(file_img)
    
    pred_rst[nn] = classifier.predict_image(im)[0]
    
print()

pred_rst = np.array(pred_rst)
print(pred_rst.shape)
    
with open(save_name, 'wb') as fh:
    pickle.dump(pred_rst, fh)
    