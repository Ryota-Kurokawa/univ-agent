import networkx as nx
import matplotlib.pyplot as plt
import random
import math
import copy

# pydotの有無をチェックし、なければspring_layoutに切り替える
try:
    import pydot
    from networkx.drawing.nx_pydot import graphviz_layout
    LAYOUT_ENGINE = "graphviz"
    print("✓ pydotライブラリが見つかりました。階層レイアウトを使用します。")
except ImportError:
    LAYOUT_ENGINE = "spring"
    print("警告: 'pydot'またはGraphviz本体が見つかりません。代替のspring_layoutで描画します。")
    print("      綺麗な階層レイアウトを使用するには、Graphvizとpydotをインストールしてください。")


class Agent:
    """エージェントを定義するクラス。"""
    def __init__(self, agent_id, initial_node, initial_info=None):
        self.agent_id = agent_id
        self.position = initial_node
        self.information = {initial_info} if initial_info else set()
        if not agent_id.startswith("R"):
            print(f"エージェント {self.agent_id} が生成されました。初期位置: {self.position}")


class Environment:
    """エージェントが活動する環境を定義するクラス。"""
    def __init__(self, branches=2, height=3):
        self.G = nx.balanced_tree(branches, height)
        self.agents = {}
        self.agent_counter = 0
        
        if LAYOUT_ENGINE == "graphviz":
            self.pos = graphviz_layout(self.G, prog='twopi', root=0)
        else:
            self.pos = nx.spring_layout(self.G, seed=42, iterations=100)

        total_nodes = len(self.G.nodes)
        print(f"平衡木グラフ環境が生成されました (分岐数:{branches}, 高さ:{height}, 総ノード数:{total_nodes})。")

    def add_agent(self, agent_id, start_node, initial_info=None):
        if start_node not in self.G.nodes():
            return None
        agent = Agent(agent_id, start_node, initial_info)
        self.agents[agent_id] = agent
        if agent_id.startswith("R"):
             print(f"新しいエージェント {agent_id} がノード {start_node} に出現しました！")
        else:
            print(f"エージェント {agent_id} がノード {start_node} に配置されました。")
        return agent

    def spawn_new_agents(self, probability=0.08):
        spawned_this_step = False
        for node in self.G.nodes():
            if random.random() < probability:
                new_agent_id = f"R{self.agent_counter}"
                self.agent_counter += 1
                self.add_agent(new_agent_id, node, initial_info=f"情報_{new_agent_id}")
                spawned_this_step = True
        return spawned_this_step

    def remove_agents(self, probability=0.05):
        agents_to_remove = []
        for agent_id in self.agents.keys():
            if random.random() < probability:
                agents_to_remove.append(agent_id)
        
        if agents_to_remove:
            for agent_id in agents_to_remove:
                print(f"エージェント {agent_id} が消失しました。")
                del self.agents[agent_id]
            return True
        return False

    def draw_environment(self, filename="environment.png", ax=None, title=None, agents_to_draw=None):
        agents_info = agents_to_draw if agents_to_draw is not None else self.agents

        create_new_figure = (ax is None)
        if create_new_figure:
            plt.figure(figsize=(8, 8))
            ax = plt.gca()
        ax.clear()

        nx.draw_networkx_nodes(self.G, self.pos, ax=ax, node_color='lightgreen', node_size=400)
        nx.draw_networkx_edges(self.G, self.pos, ax=ax, edge_color='gray', width=1.0, alpha=0.8)
        nx.draw_networkx_labels(self.G, self.pos, ax=ax, font_size=8, font_color='black')

        agent_positions = {agent.agent_id: agent.position for agent in agents_info.values()}
        agent_nodes = list(agent_positions.values())
        nx.draw_networkx_nodes(self.G, self.pos, ax=ax, nodelist=agent_nodes, node_color='tomato', node_size=500)
        
        label_offset = 20 if LAYOUT_ENGINE == "graphviz" else 0.05
        for agent_id, node in agent_positions.items():
            x, y = self.pos[node]
            ax.text(x, y + label_offset, s=agent_id,
                     bbox=dict(facecolor='tomato', alpha=0.8),
                     horizontalalignment='center', fontsize=9, color='white', fontweight='bold')

        default_title = "Environment State"
        ax.set_title(title if title else default_title, fontsize=14)
        ax.axis('off')

        if create_new_figure:
            plt.tight_layout()
            plt.savefig(filename)
            plt.close()
            print(f"✓ 環境の状態を {filename} に保存しました。")


# ★★★修正ポイント1: イベント情報をグラフ内に直接テキストで描画★★★
def draw_simulation_grid(env, history, filename="simulation_steps.png", start_step_number=0):
    steps_in_this_image = len(history)
    if steps_in_this_image == 0: return

    cols = 3
    rows = math.ceil(steps_in_this_image / cols)
    fig, axes = plt.subplots(rows, cols, figsize=(cols * 5, rows * 5.2), squeeze=False)
    axes_flat = axes.flatten()

    print(f"\n--- シミュレーション履歴の描画開始 (ステップ {start_step_number + 1}から) ---")
    
    for i, snapshot in enumerate(history):
        ax = axes_flat[i]
        
        # 1. 基本的なタイトルを設定
        step_title = f"Step {start_step_number + i + 1}"
        
        # 2. グラフ本体を描画
        env.draw_environment(
            ax=ax,
            title=step_title,
            agents_to_draw=snapshot['agents']
        )
        
        # 3. イベント情報をテキストとしてグラフの左上に描画
        events = []
        if snapshot['spawned']:
            events.append("+発生")
        if snapshot['removed']:
            events.append("-消失")
        
        if events:
            event_text = ' '.join(events)
            # Axes座標系(左下(0,0), 右上(1,1))の左上にテキストを配置
            ax.text(0.03, 0.97, event_text, 
                    transform=ax.transAxes, 
                    fontsize=12, 
                    fontweight='bold',
                    color='darkred', 
                    ha='left', 
                    va='top', 
                    bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', pad=0.2))

    for j in range(steps_in_this_image, len(axes_flat)):
        axes_flat[j].axis('off')

    fig.suptitle(f"Simulation Steps: {start_step_number + 1} - {start_step_number + steps_in_this_image}", fontsize=16)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(filename)
    plt.close()
    print(f"✓ ステップ {start_step_number + 1} からの履歴を {filename} に保存しました。")


# --- メインの処理 ---
if __name__ == "__main__":
    print("--- シミュレーション設定 ---")
    env = Environment(branches=2, height=3)

    agent1 = env.add_agent("A1", 0, "情報_アルファ")
    outer_nodes = [node for node, degree in env.G.degree() if degree == 1]
    if outer_nodes:
      agent2 = env.add_agent("B2", random.choice(outer_nodes), "情報_ベータ")

    env.draw_environment(filename="initial_state_tree.png", title="Initial State")

    simulation_steps = 10
    new_agent_probability = 0.08
    agent_disappearance_rate = 0.05

    print(f"\n--- {simulation_steps}ステップのシミュレーション開始 ---")
    print(f"(出現率: {new_agent_probability*100:.0f}%, 消失率: {agent_disappearance_rate*100:.0f}%)")
    
    history = []
    for i in range(simulation_steps):
        print(f"\n--- ステップ {i+1} ---")
        
        for agent_id, agent in env.agents.items():
            neighbors = list(env.G.neighbors(agent.position))
            if neighbors:
                new_position = random.choice(neighbors)
                agent.position = new_position
                print(f"エージェント {agent_id} がノード {new_position} に移動しました。")
        
        # エージェントの生成・削除を無効化
        # has_spawned = env.spawn_new_agents(probability=new_agent_probability)
        # has_removed = env.remove_agents(probability=agent_disappearance_rate)
        has_spawned = False
        has_removed = False
        
        # イベントの有無も一緒に履歴に保存
        snapshot = {
            'agents': copy.deepcopy(env.agents),
            'spawned': has_spawned,
            'removed': has_removed
        }
        history.append(snapshot)

    steps_per_image = 6
    total_steps = len(history)
    num_images = math.ceil(total_steps / steps_per_image)

    for i in range(num_images):
        start_index = i * steps_per_image
        end_index = start_index + steps_per_image
        history_chunk = history[start_index:end_index]
        
        filename = f"simulation_steps_part_{i+1}.png"
        draw_simulation_grid(env, history_chunk, filename, start_step_number=start_index)
        
    print("\n--- シミュレーション完了 ---")