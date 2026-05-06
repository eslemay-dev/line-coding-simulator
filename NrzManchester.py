import tkinter as tk
from tkinter import ttk, messagebox
import math

# ─────────────────────────────────────────────
#   KODLAMA FONKSİYONLARI
# ─────────────────────────────────────────────
def encode_nrzl(bit_dizisi):
    return ['H' if b == '1' else 'L' for b in bit_dizisi]

def encode_manchester(bit_dizisi):
    sonuc = []
    for b in bit_dizisi:
        sonuc += ['H', 'L'] if b == '1' else ['L', 'H']
    return sonuc

# ─────────────────────────────────────────────
#   RENK PALETİ
# ─────────────────────────────────────────────
BG        = "#0f1117"
PANEL     = "#1a1d27"
CARD      = "#22263a"
ACCENT    = "#4f8ef7"
ACCENT2   = "#7c3aed"
SUCCESS   = "#22d3a5"
WARNING   = "#f59e0b"
TEXT      = "#e8eaf6"
TEXT_DIM  = "#7986a8"
BORDER    = "#2e3250"
H_COLOR   = "#4ade80"
L_COLOR   = "#f87171"

# ─────────────────────────────────────────────
#   ANA UYGULAMA SINIFI
# ─────────────────────────────────────────────
class HatKodlamaApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hat Kodlama & Fiziksel Katman Gecikme Hesaplayıcı")
        self.geometry("980x760")
        self.resizable(True, True)
        self.configure(bg=BG)
        self._build_ui()

    # ── UI İnşası ────────────────────────────
    def _build_ui(self):
        self._header()
        main = tk.Frame(self, bg=BG)
        main.pack(fill="both", expand=True, padx=18, pady=(0, 18))
        main.columnconfigure(0, weight=1)
        main.columnconfigure(1, weight=1)
        main.rowconfigure(0, weight=0)
        main.rowconfigure(1, weight=1)

        self._input_panel(main)
        self._result_panel(main)
        self._signal_canvas(main)

    def _header(self):
        hf = tk.Frame(self, bg=ACCENT2, height=4)
        hf.pack(fill="x")

        header = tk.Frame(self, bg=PANEL, pady=16)
        header.pack(fill="x", padx=0)

        tk.Label(header, text="⬡  HAT KODLAMA & GECİKME HESAPLAYICI",
                 font=("Courier New", 16, "bold"),
                 bg=PANEL, fg=ACCENT).pack(side="left", padx=24)
        tk.Label(header,
                 text="Bilgisayar Ağları — Fiziksel Katman",
                 font=("Courier New", 10),
                 bg=PANEL, fg=TEXT_DIM).pack(side="right", padx=24)

    def _input_panel(self, parent):
        frame = tk.Frame(parent, bg=CARD, bd=0,
                         highlightbackground=BORDER, highlightthickness=1)
        frame.grid(row=0, column=0, sticky="nsew", padx=(0, 8), pady=(12, 8))
        frame.columnconfigure(1, weight=1)

        tk.Label(frame, text="● GİRİŞ PARAMETRELERİ",
                 font=("Courier New", 11, "bold"),
                 bg=CARD, fg=ACCENT).grid(
                     row=0, column=0, columnspan=2,
                     sticky="w", padx=16, pady=(14, 10))

        # Bit dizisi
        self._lbl(frame, "Bit Dizisi", 1)
        self.bit_var = tk.StringVar(value="10110010")
        self._entry(frame, self.bit_var, 1, "örnek: 101001")

        # Kodlama seçimi
        self._lbl(frame, "Kodlama Türü", 2)
        self.kod_var = tk.StringVar(value="NRZ-L")
        kod_frame = tk.Frame(frame, bg=CARD)
        kod_frame.grid(row=2, column=1, sticky="w", padx=(0, 16), pady=4)
        for txt in ("NRZ-L", "MANCHESTER"):
            tk.Radiobutton(kod_frame, text=txt, variable=self.kod_var, value=txt,
                           bg=CARD, fg=TEXT, selectcolor=ACCENT2,
                           activebackground=CARD, activeforeground=ACCENT,
                           font=("Courier New", 10)).pack(side="left", padx=(0, 12))

        # Sayısal girdiler
        self._lbl(frame, "Bit Hızı R (bps)", 3)
        self.r_var = tk.StringVar(value="1000000")
        self._entry(frame, self.r_var, 3, "örnek: 1000000")

        self._lbl(frame, "Uzunluk d (metre)", 4)
        self.d_var = tk.StringVar(value="500")
        self._entry(frame, self.d_var, 4, "örnek: 500")

        self._lbl(frame, "Yayılma Hızı v (m/s)", 5)
        self.v_var = tk.StringVar(value="200000000")
        self._entry(frame, self.v_var, 5, "örnek: 2e8")

        # Hesapla butonu
        btn = tk.Button(frame, text="▶  HESAPLA",
                        command=self._hesapla,
                        font=("Courier New", 12, "bold"),
                        bg=ACCENT, fg="white",
                        activebackground=ACCENT2, activeforeground="white",
                        relief="flat", cursor="hand2", pady=8)
        btn.grid(row=6, column=0, columnspan=2,
                 sticky="ew", padx=16, pady=(14, 16))

    def _result_panel(self, parent):
        frame = tk.Frame(parent, bg=CARD,
                         highlightbackground=BORDER, highlightthickness=1)
        frame.grid(row=0, column=1, sticky="nsew", padx=(8, 0), pady=(12, 8))
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)

        tk.Label(frame, text="● SONUÇLAR",
                 font=("Courier New", 11, "bold"),
                 bg=CARD, fg=SUCCESS).grid(
                     row=0, column=0, sticky="w", padx=16, pady=(14, 6))

        self.result_text = tk.Text(
            frame, bg=PANEL, fg=TEXT,
            font=("Courier New", 10),
            relief="flat", bd=0,
            state="disabled",
            wrap="word",
            insertbackground=ACCENT)
        self.result_text.grid(row=1, column=0, sticky="nsew",
                              padx=10, pady=(0, 12))

        sb = ttk.Scrollbar(frame, command=self.result_text.yview)
        sb.grid(row=1, column=1, sticky="ns", pady=(0, 12))
        self.result_text.configure(yscrollcommand=sb.set)

        # renk tag'leri
        self.result_text.tag_config("title",   foreground=ACCENT,   font=("Courier New", 10, "bold"))
        self.result_text.tag_config("value",   foreground=SUCCESS)
        self.result_text.tag_config("warning", foreground=WARNING)
        self.result_text.tag_config("dim",     foreground=TEXT_DIM)
        self.result_text.tag_config("sep",     foreground=BORDER)

    def _signal_canvas(self, parent):
        frame = tk.Frame(parent, bg=CARD,
                         highlightbackground=BORDER, highlightthickness=1)
        frame.grid(row=1, column=0, columnspan=2,
                   sticky="nsew", padx=0, pady=(8, 0))
        frame.rowconfigure(1, weight=1)
        frame.columnconfigure(0, weight=1)

        tk.Label(frame, text="● SİNYAL DİYAGRAMI",
                 font=("Courier New", 11, "bold"),
                 bg=CARD, fg=WARNING).grid(
                     row=0, column=0, sticky="w", padx=16, pady=(12, 4))

        self.canvas = tk.Canvas(frame, bg=PANEL,
                                highlightthickness=0, height=180)
        self.canvas.grid(row=1, column=0, sticky="nsew",
                         padx=12, pady=(0, 12))

    # ── Yardımcı widget'lar ──────────────────
    def _lbl(self, parent, text, row):
        tk.Label(parent, text=text + " :",
                 font=("Courier New", 10),
                 bg=CARD, fg=TEXT_DIM,
                 anchor="e").grid(row=row, column=0,
                                  sticky="e", padx=(16, 8), pady=4)

    def _entry(self, parent, var, row, placeholder=""):
        e = tk.Entry(parent, textvariable=var,
                     font=("Courier New", 11),
                     bg=PANEL, fg=TEXT,
                     insertbackground=ACCENT,
                     relief="flat", bd=6)
        e.grid(row=row, column=1, sticky="ew",
               padx=(0, 16), pady=4)

    # ── Hesaplama mantığı ────────────────────
    def _hesapla(self):
        # Doğrulama
        bit = self.bit_var.get().strip()
        if not bit:
            messagebox.showerror("Hata", "Bit dizisi boş olamaz!")
            return
        if not all(c in '01' for c in bit):
            messagebox.showerror("Hata", "Sadece 0 ve 1 girilebilir!")
            return

        try:
            R = float(self.r_var.get())
            d = float(self.d_var.get())
            v = float(self.v_var.get())
        except ValueError:
            messagebox.showerror("Hata", "R, d, v sayısal olmalıdır!")
            return

        if R <= 0 or v <= 0 or d < 0:
            messagebox.showerror("Hata", "R ve v pozitif, d ≥ 0 olmalı!")
            return

        # Kodlama
        kodlama = self.kod_var.get()
        semboller = encode_nrzl(bit) if kodlama == "NRZ-L" else encode_manchester(bit)
        n = len(bit)

        # Gecikmeler
        td = n / R
        pd = d / v
        total = td + pd

        # Sonuç metnini yaz
        self._write_results(bit, n, kodlama, semboller, R, d, v, td, pd, total)
        # Sinyal çiz
        self._draw_signal(bit, kodlama, semboller)

    def _write_results(self, bit, n, kodlama, semboller, R, d, v, td, pd, total):
        t = self.result_text
        t.configure(state="normal")
        t.delete("1.0", "end")

        def w(text, tag=None):
            t.insert("end", text, tag)

        w("━" * 44 + "\n", "sep")
        w(" GİRİŞ\n", "title")
        w("━" * 44 + "\n", "sep")
        w(f"  Bit Dizisi     : "); w(f"{bit}  ({n} bit)\n", "value")
        w(f"  Kodlama        : "); w(f"{kodlama}\n", "value")
        w(f"  Sembol Çıktı   : "); w(f"{' '.join(semboller)}\n", "value")
        w(f"  Sembol Sayısı  : "); w(f"{len(semboller)}\n", "value")
        w("\n")

        w("━" * 44 + "\n", "sep")
        w(" GECİKME HESAPLARI\n", "title")
        w("━" * 44 + "\n", "sep")
        w(f"\n  Transmission Delay\n", "warning")
        w(f"    = n / R  =  {n} / {R:.0f}\n", "dim")
        w(f"    = {td:.6e} saniye\n\n", "value")

        w(f"  Propagation Delay\n", "warning")
        w(f"    = d / v  =  {d:.0f} / {v:.2e}\n", "dim")
        w(f"    = {pd:.6e} saniye\n\n", "value")

        w(f"  Toplam Gecikme\n", "warning")
        w(f"    = {td:.6e} + {pd:.6e}\n", "dim")
        w(f"    = {total:.6e} saniye\n\n", "value")

        w("━" * 44 + "\n", "sep")
        w(" KODLAMA NOTU\n", "title")
        w("━" * 44 + "\n", "sep")
        if kodlama == "NRZ-L":
            w("  • Bit başına 1 sinyal seviyesi\n", "dim")
            w("  • Düşük bant genişliği\n", "dim")
            w("  • Uzun serilerde senkron sorunu\n", "dim")
        else:
            w("  • Bit başına 2 yarı-periyot (HL / LH)\n", "dim")
            w("  • Kendi kendine senkronizasyon\n", "dim")
            w("  • 2× bant genişliği gerektirir\n", "dim")
        w("━" * 44 + "\n", "sep")

        t.configure(state="disabled")

    # ── Sinyal diyagramı ─────────────────────
    def _draw_signal(self, bit, kodlama, semboller):
        c = self.canvas
        c.delete("all")
        c.update_idletasks()

        W = c.winfo_width() or 900
        H = c.winfo_height() or 180

        pad_l, pad_r = 60, 20
        pad_t, pad_b = 30, 40
        sig_w = W - pad_l - pad_r
        sig_h = H - pad_t - pad_b

        mid_y   = pad_t + sig_h * 0.5
        high_y  = pad_t + sig_h * 0.15
        low_y   = pad_t + sig_h * 0.85

        total_sym = len(semboller)
        sym_w = sig_w / total_sym

        # Izgara çizgileri
        for y, label, col in [(high_y, "H", H_COLOR), (mid_y, "─", TEXT_DIM), (low_y, "L", L_COLOR)]:
            c.create_line(pad_l, y, W - pad_r, y,
                          fill=BORDER, dash=(4, 6), width=1)
            c.create_text(pad_l - 8, y, text=label,
                          fill=col, font=("Courier New", 9, "bold"), anchor="e")

        # Başlık
        c.create_text(W // 2, 12,
                      text=f"{'NRZ-L' if kodlama=='NRZ-L' else 'Manchester'} Kodlanmış Sinyal — {bit}",
                      fill=TEXT_DIM, font=("Courier New", 9))

        # Semboller
        def y_of(sym):
            return high_y if sym == 'H' else low_y

        prev_y = y_of(semboller[0])
        for i, sym in enumerate(semboller):
            x1 = pad_l + i * sym_w
            x2 = x1 + sym_w
            cur_y = y_of(sym)
            col = H_COLOR if sym == 'H' else L_COLOR

            # Dikey geçiş
            if cur_y != prev_y:
                c.create_line(x1, prev_y, x1, cur_y, fill=ACCENT, width=2)

            # Yatay çizgi
            c.create_line(x1, cur_y, x2, cur_y, fill=col, width=2.5)

            # Bit etiketleri (NRZ-L: her sembol = 1 bit, Manchester: 2 sembol = 1 bit)
            if kodlama == "NRZ-L":
                mid_x = x1 + sym_w / 2
                c.create_text(mid_x, low_y + 18,
                               text=bit[i], fill=TEXT_DIM,
                               font=("Courier New", 9))
                c.create_line(x1, low_y + 8, x1, low_y + 12,
                               fill=BORDER, width=1)
            else:
                if i % 2 == 0:
                    bit_idx = i // 2
                    mid_x = x1 + sym_w
                    c.create_text(mid_x, low_y + 18,
                                   text=bit[bit_idx] if bit_idx < len(bit) else "",
                                   fill=TEXT_DIM,
                                   font=("Courier New", 9))
                    c.create_line(x1, low_y + 8, x1, low_y + 12,
                                   fill=BORDER, width=1)

            prev_y = cur_y

        # Son dikey sınır
        x_end = pad_l + total_sym * sym_w
        c.create_line(x_end, high_y, x_end, low_y,
                       fill=BORDER, dash=(4, 4), width=1)

        # X ekseni
        c.create_line(pad_l, low_y + 6, W - pad_r, low_y + 6,
                       fill=BORDER, width=1)


# ─────────────────────────────────────────────
if __name__ == "__main__":
    app = HatKodlamaApp()
    app.mainloop()