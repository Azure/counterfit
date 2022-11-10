from .DCPW import DeepCPWrapper
import gzip
import pickle
import numpy as np
import os
import json
import sys
from PIL import Image


def writeVideo(fname,frames,fps=20):
    images = []
    for i, frame in enumerate(frames):
        frame = np.transpose(frame, (1,2,0))[:,:,::-1]  # convert BGR to RGB
        frame = (frame*255).astype(np.uint8)  # convert to uint8
        im = Image.fromarray(frame)
        im_size = im.size
        im = im.resize((im_size[0]*6, im_size[1]*6))
        images.append(im)
    images[0].save(fname, save_all=True, append_images=images[1:], duration=int(1000/fps), loop=0)
    return images


def main(args):
    path = args['path']
    results = {}
    data_path = os.path.join(path, "cartpole_samples_10000_100.pkl.gz")
    # original video
    with gzip.open(data_path,'r') as infile:
        data = pickle.load(infile)
    frames = np.array(data).reshape(-1, 3, 40, 90)
    # simulation environment
    init_state_path = os.path.join(path, "cartpole_samples_10000_100_init_state.gz")
    init_state = pickle.load(gzip.open(init_state_path, 'rb'))
    if args["attack_id"] is not None:    
        attack_id = args['attack_id']
        writeVideo(os.path.join(path, 'results', attack_id, 'original_%s.gif' % attack_id), frames)
        attack_path = os.path.join(path, "results", attack_id)
        results['cart_pole'] = os.path.join(attack_path, "run_summary.json")
        
        # cart-pole
        with open(results['cart_pole'], 'r') as infile:
            data = json.load(infile)['results']

        noisy_frames = np.array(data).reshape(-1, 3, 40, 90)
        writeVideo(os.path.join(attack_path, 'cartpole.gif'), noisy_frames)
        
        dcpw = DeepCPWrapper()
        # cart-pole: what actually happened
        done, n_steps, _, final_state, actual_frames = dcpw.replay(noisy_frames, max_steps=len(frames), init_state=init_state, return_actual_frames=True)
        actual_frames = np.array(actual_frames).reshape(-1, 3, 40, 90)
        writeVideo(os.path.join(attack_path, 'cartpole_actual.gif'), actual_frames)

    # what's the difference between two images?
    # ffmpeg -i "original.gif" -i "cartpole_actual.gif" -filter_complex "blend=difference" cartpole_actual_blended.gif

    # cart-pole-init state
    if args["init_attack_id"] is not None:
        
        init_attack_id = args['init_attack_id']
        writeVideo(os.path.join(path, 'results', init_attack_id, 'original_%s.gif' % init_attack_id), frames)
        
        init_attack_path = os.path.join(path, "results", init_attack_id)
        results['cart_pole_init_state'] = os.path.join(init_attack_path, "run_summary.json")
        with open(results['cart_pole_init_state'], 'r') as infile:
            tweaked_init_state = np.array(json.load(infile)['results'][0], dtype=np.float32)
        dcpw = DeepCPWrapper()
        #Create gif of original and perturbed initial states
        init_states = []
        frames_init_state_original, _, _ = dcpw.play(max_steps=1, init_state=init_state, play_to_end=True)
        frames_init_state_tweaked, _, _ = dcpw.play(max_steps=1, init_state=tweaked_init_state, play_to_end=True)
        print(init_state)
        print(tweaked_init_state)
        init_states.append(frames_init_state_original[0])
        init_states.append(frames_init_state_tweaked[0])
        init_states = np.array(init_states, dtype=np.float32).squeeze()
        fname = os.path.join(path, 'results', init_attack_id, 'original_tweaked_init_%s.gif' % init_attack_id)
        images = writeVideo(fname, init_states, fps=1)
        images[0].save(os.path.join(path, 'results', init_attack_id, 'initial_position_%s.png' % init_attack_id),"PNG")
        images[1].save(os.path.join(path, 'results', init_attack_id, 'perturbed_initial_position_%s.png' % init_attack_id),"PNG")
        
        #Create gif of full set of states from perturbed initial state
        frames_init_state, _, _ = dcpw.play(max_steps=len(frames), init_state=tweaked_init_state, play_to_end=True)
        frames_init_state = np.array(frames_init_state, dtype=np.float32).squeeze()
        writeVideo(os.path.join(init_attack_path, 'cartpole_initstate.gif'), frames_init_state)

      
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Program to generate gif videos for cartpole')
    parser.add_argument('-p','--path', help='Relative path where results dir is located', default='counterfit/targets/cart_pole', required=False)
    parser.add_argument('-a','--attack_id', help='ID of attack to animate', default=None, required=False)
    parser.add_argument('-i','--init_attack_id', help='ID of init_state attack to animate', default=None, required=False)
    args = vars(parser.parse_args())
    if args["attack_id"] is None and args["init_attack_id"] is None:
        print("Need to specify either attack_id or init_attack_id to generate video")
        sys.exit(1)
    main(args)

