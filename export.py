"""
Utilitários para exportar traduções
Use este módulo para salvar histórico de traduções
"""

import json
import csv
from datetime import datetime
from pathlib import Path

class TranslationExporter:
    def __init__(self, output_dir="exports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.history = []
    
    def add_translation(self, gesto, confianca, timestamp=None):
        """Adiciona uma tradução ao histórico"""
        if timestamp is None:
            timestamp = datetime.now()
        
        self.history.append({
            'gesto': gesto,
            'confianca': confianca,
            'timestamp': timestamp.isoformat(),
            'data': timestamp.strftime('%d/%m/%Y'),
            'hora': timestamp.strftime('%H:%M:%S')
        })
    
    def export_txt(self, filename=None):
        """Exporta para arquivo TXT"""
        if filename is None:
            filename = f"traducoes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        filepath = self.output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("="*60 + "\n")
            f.write("HISTÓRICO DE TRADUÇÕES - LIBRAS BRIDGE\n")
            f.write("="*60 + "\n\n")
            
            for item in self.history:
                f.write(f"Data: {item['data']} às {item['hora']}\n")
                f.write(f"Gesto: {item['gesto'].upper()}\n")
                f.write(f"Confiança: {item['confianca']}%\n")
                f.write("-"*60 + "\n\n")
            
            f.write(f"\nTotal de traduções: {len(self.history)}\n")
        
        print(f"✅ Exportado para: {filepath}")
        return str(filepath)
    
    def export_csv(self, filename=None):
        """Exporta para arquivo CSV"""
        if filename is None:
            filename = f"traducoes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        filepath = self.output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['data', 'hora', 'gesto', 'confianca'])
            writer.writeheader()
            writer.writerows(self.history)
        
        print(f"✅ Exportado para: {filepath}")
        return str(filepath)
    
    def export_json(self, filename=None):
        """Exporta para arquivo JSON"""
        if filename is None:
            filename = f"traducoes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        filepath = self.output_dir / filename
        
        data = {
            'metadata': {
                'total_traducoes': len(self.history),
                'exportado_em': datetime.now().isoformat(),
                'sistema': 'Libras Bridge v1.0'
            },
            'traducoes': self.history
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Exportado para: {filepath}")
        return str(filepath)
    
    def export_statistics(self, filename=None):
        """Exporta estatísticas das traduções"""
        if filename is None:
            filename = f"estatisticas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        filepath = self.output_dir / filename
        
        # Calcular estatísticas
        gestos_count = {}
        confianca_total = 0
        
        for item in self.history:
            gesto = item['gesto']
            gestos_count[gesto] = gestos_count.get(gesto, 0) + 1
            confianca_total += item['confianca']
        
        confianca_media = confianca_total / len(self.history) if self.history else 0
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("="*60 + "\n")
            f.write("ESTATÍSTICAS - LIBRAS BRIDGE\n")
            f.write("="*60 + "\n\n")
            
            f.write(f"Total de traduções: {len(self.history)}\n")
            f.write(f"Confiança média: {confianca_media:.2f}%\n\n")
            
            f.write("Gestos mais usados:\n")
            f.write("-"*60 + "\n")
            
            sorted_gestos = sorted(gestos_count.items(), key=lambda x: x[1], reverse=True)
            for gesto, count in sorted_gestos:
                percentage = (count / len(self.history)) * 100
                f.write(f"  {gesto.upper()}: {count} vezes ({percentage:.1f}%)\n")
            
            f.write("\n" + "="*60 + "\n")
        
        print(f"✅ Estatísticas exportadas para: {filepath}")
        return str(filepath)
    
    def clear_history(self):
        """Limpa o histórico"""
        self.history.clear()
        print("✅ Histórico limpo")
    
    def get_summary(self):
        """Retorna resumo do histórico"""
        if not self.history:
            return "Nenhuma tradução registrada"
        
        gestos_count = {}
        for item in self.history:
            gesto = item['gesto']
            gestos_count[gesto] = gestos_count.get(gesto, 0) + 1
        
        return {
            'total': len(self.history),
            'gestos': gestos_count,
            'primeiro': self.history[0],
            'ultimo': self.history[-1]
        }


# Exemplo de uso
if __name__ == "__main__":
    print("="*60)
    print("TESTANDO EXPORTADOR DE TRADUÇÕES")
    print("="*60 + "\n")
    
    # Criar exportador
    exporter = TranslationExporter()
    
    # Adicionar traduções de exemplo
    from datetime import datetime, timedelta
    
    base_time = datetime.now() - timedelta(minutes=10)
    
    gestos_exemplo = [
        ('ola', 92), ('sim', 88), ('nao', 95),
        ('ola', 91), ('sim', 87), ('obrigado', 89),
        ('nao', 93), ('ola', 90)
    ]
    
    for i, (gesto, conf) in enumerate(gestos_exemplo):
        timestamp = base_time + timedelta(seconds=i*15)
        exporter.add_translation(gesto, conf, timestamp)
    
    print(f"✅ {len(gestos_exemplo)} traduções adicionadas\n")
    
    # Exportar em todos os formatos
    print("Exportando...")
    exporter.export_txt()
    exporter.export_csv()
    exporter.export_json()
    exporter.export_statistics()
    
    # Mostrar resumo
    print("\n" + "="*60)
    print("RESUMO")
    print("="*60)
    summary = exporter.get_summary()
    print(json.dumps(summary, indent=2, ensure_ascii=False))