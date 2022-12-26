import yaml
import argparse
import body
import movement_reader
import pynput

class KinectController():
    def __init__(self):
        parser = argparse.ArgumentParser('KinectController')
        parser.add_argument('--config', '-c', type=str, default='config.yaml')

        arguments = parser.parse_args()

        with open(arguments.config, 'r') as configFile:
            self.config = yaml.load(configFile)

        def player_create(config):
            return {
                'config': config,
                'parser': movement_reader.MovementReader()
            }

        self.players = map(player_create, self.config['players'])

        self.keyboard = pynput.keyboard.Controller()

    def parse_body(
        self,
        body # type: body.Body
    ):
        head_x = body.get_joint_Head().x

        for player in self.players:
            config = player['config']
            try:
                side = config['side']
                if side == 'left' and head_x > 0:
                    # player on wrong side
                    continue
                if side == 'right' and head_x < 0:
                    # player on wrong side
                    continue
            except KeyError:
                # player has no side set, aka can be on whole screen
                pass

            parser = player['parser'] # type: movement_reader.MovementReader
            parser.parse_movement(body)

            move_action_mapping = {
                'run': parser.isRunning,
                'run_right': parser.isRunning and not parser.isRunningLeft,
                'run_left': parser.isRunning and parser.isRunningLeft,
                'jump': parser.isJumping,
                'item': parser.isUsingItem,
                'hook': parser.isHandUp,
                'dodge': parser.isDodging
            }

            def find_key_by_action(action_label):
                try:
                    if config['actions'] is None:
                        return None
                    for action in config['actions']:
                        if action['action'] == action_label:
                            return action
                    return None
                except KeyError:
                    pass

            for key in move_action_mapping.keys():
                keyboard_key = find_key_by_action(key)
                if keyboard_key is None:
                    # action irrelevant
                    continue
                
                key_value = keyboard_key['key']
                try:
                    key_value = pynput.keyboard.Key._member_map_[key_value]
                except KeyError:
                    # key not found, could be something like "a" that doesn't need translation
                    pass

                if move_action_mapping[key]:
                    self.keyboard.press(key_value)
                else:
                    self.keyboard.release(key_value)

            return player

