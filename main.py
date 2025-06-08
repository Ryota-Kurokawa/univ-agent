import networkx as nx
import matplotlib.pyplot as plt
import random

class Agent:
    """
    エージェントを定義するクラス。
    """
    def __init__(self, agent_id, initial_node, initial_info=None):
        """
        エージェントを初期化する。
        - agent_id: エージェントのユニークなID (例: "A1")
        - initial_node: エージェントの初期配置ノード。タプル(x, y)で指定。
        - initial_info: エージェントが最初に持っている情報
        """
        self.agent_id = agent_id
        self.position = initial_node # positionは(x, y)のタプル
        self.information = {initial_info} if initial_info else set()
        print(f"エージェント {self.agent_id} が生成されました。初期位置: {self.position}")


class Environment:
    """
    エージェントが活動する環境を定義するクラス。
    グラフ構造やエージェントの管理を行う。
    """
    def __init__(self, width=10, height=10):
        """
        環境を初期化する。
        - width, height: 環境の格子のサイズ
        """
        # ★変更点: 10x10の格子状のグラフを生成
        # ノードは (x, y) というタプルで表現される (例: (0,0), (0,1), ...)
        self.G = nx.grid_2d_graph(width, height)
        self.agents = {} # エージェントをIDとオブジェクトの辞書として管理
        print(f"{width}x{height}の格子状環境が生成されました。")

    def add_agent(self, agent_id, start_node, initial_info=None):
        """
        環境に新しいエージェントを追加する。
        - start_node: (x, y)のタプル
        """
        if start_node not in self.G.nodes():
            print(f"エラー: ノード {start_node} は環境内に存在しません。")
            return None

        agent = Agent(agent_id, start_node, initial_info)
        self.agents[agent_id] = agent
        print(f"エージェント {agent_id} がノード {start_node} に配置されました。")
        return agent

    def draw_environment(self, filename="environment.png"):
        """
        現在の環境（グラフとエージェントの位置）を描画し、画像ファイルとして保存する。
        """
        plt.figure(figsize=(10, 10)) # 正方形に近づけるためサイズ調整
        ax = plt.gca() # 現在の軸情報を取得

        # ★変更点: ノードの位置をグラフの座標そのものに設定
        # これにより、ノードがグリッドの交点に正確に配置される
        pos = {node: node for node in self.G.nodes()}

        # ★追加点: 背景にグリッドを描画
        ax.set_xticks(range(10))
        ax.set_yticks(range(10))
        ax.set_xlim(-0.5, 9.5)
        ax.set_ylim(-0.5, 9.5)
        plt.grid(True, linestyle='--', color='lightgray')

        # グラフの描画
        nx.draw_networkx_nodes(self.G, pos, node_color='lightblue', node_size=300)
        nx.draw_networkx_edges(self.G, pos, edge_color='gray')
        # ノードラベルは情報量が多すぎるので描画しない

        # エージェントの位置とIDを取得
        agent_positions = [agent.position for agent in self.agents.values()]
        agent_labels = {agent.agent_id: agent.position for agent in self.agents.values()}

        # エージェントがいるノードを色を変えて描画
        nx.draw_networkx_nodes(self.G, pos, nodelist=agent_positions, node_color='tomato', node_size=400)
        
        # エージェントIDをノードの少し下に表示
        for agent_id, node in agent_labels.items():
            x, y = pos[node]
            plt.text(x, y - 0.3, s=agent_id,
                     bbox=dict(facecolor='tomato', alpha=0.8),
                     horizontalalignment='center',
                     fontsize=9,
                     color='white',
                     fontweight='bold')

        plt.title("Environment State", fontsize=16)
        # ★追加点: アスペクト比を固定してマス目を正方形にする
        ax.set_aspect('equal', adjustable='box')
        plt.savefig(filename)
        plt.close()
        print(f"✓ 環境の状態を {filename} に保存しました。")


# --- メインの処理 ---
if __name__ == "__main__":
    print("--- シミュレーション設定 ---")
    # ★変更点: 10x10の環境を作成
    env = Environment(width=10, height=10)

    # ★変更点: エージェントの初期位置を(x, y)タプルで指定
    agent1 = env.add_agent("A1", (0, 9), "情報_アルファ") # 左上
    agent2 = env.add_agent("B2", (9, 0), "情報_ベータ")  # 右下

    # 3. 初期状態を描画して保存
    env.draw_environment("initial_state_grid.png")

    # 4. 簡単なシミュレーションを実行
    simulation_steps = 5
    print(f"\n--- {simulation_steps}ステップのシミュレーション開始 ---")

    for i in range(simulation_steps):
        print(f"\n--- ステップ {i+1} ---")
        for agent_id, agent in env.agents.items():
            neighbors = list(env.G.neighbors(agent.position))
            if neighbors:
                new_position = random.choice(neighbors)
                agent.position = new_position
                print(f"エージェント {agent_id} がノード {new_position} に移動しました。")

        env.draw_environment(f"step_{i+1}_grid.png")

    print("\n--- シミュレーション完了 ---")